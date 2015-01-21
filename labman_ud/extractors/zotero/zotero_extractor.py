import time
import pickle
import socket

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Max
from django.template.defaultfilters import slugify

from entities.events.models import Event
from entities.persons.models import Person, Nickname
from entities.projects.models import Project, RelatedPublication
from entities.publications.models import *
from entities.utils.models import Tag, City, Country
from extractors.zotero.models import ZoteroExtractorLog
from labman_setup.models import ZoteroConfiguration
from labman_ud.util import nslugify

from entities.publications.models import QUARTILE_CHOICES, Ranking, PublicationRank

from datetime import datetime
from dateutil import parser
from pyzotero import zotero
from pyzotero.zotero_errors import HTTPError

import os
import pprint
import re


pp = pprint.PrettyPrinter(indent=4)

JCR_PATTERN = r'(jcr|if)(-*)(\d(\.|\,)\d+)'
ACCEPTED_ATTACHMENT_FORMATS = ('.pdf','.doc','.docx')

####################################################################################################
# def: get_zotero_variables()
####################################################################################################

def get_zotero_variables():
    try:
        zotero_config = ZoteroConfiguration.objects.get()

        api_key = zotero_config.api_key
        library_id = zotero_config.library_id
        library_type = zotero_config.library_type

        return api_key, library_id, library_type

    except ObjectDoesNotExist:
        print "ZoteroConfiguration object not configured in admin panel"

        return '', '', ''
        

####################################################################################################
# def: get_zotero_connection()
####################################################################################################        
def get_zotero_connection():
    api_key, library_id, library_type = get_zotero_variables()
    zot = zotero.Zotero(library_id = library_id, library_type=library_type, api_key=api_key)
    
    return zot


####################################################################################################
# def: get_last_zotero_version()
####################################################################################################

def get_last_zotero_version():
    zot = get_zotero_connection()

    NEW_ZOTERO = False
    if NEW_ZOTERO:
        latest_version_number = zot.last_modified_version()
    else:
        items = zot.items(limit=1)
        latest_version_number = int(zot.request.headers.get('last-modified-version', 0))

    return latest_version_number


####################################################################################################
# def: get_last_synchronized_zotero_version()
####################################################################################################

def get_last_synchronized_zotero_version():
    try:
        last_version = ZoteroExtractorLog.objects.all().aggregate(Max('version'))['version__max']
        if last_version is None:
            last_version = 0

    except:
        last_version = 0

    return last_version


####################################################################################################
# def: get_item_keys_since_last_synchronized_version()
####################################################################################################

def extract_publications_from_zotero(from_version):
    last_zotero_version = get_last_zotero_version()

    if from_version == last_zotero_version:
        print 'Labman is updated to the last version in Zotero (%d)' % (last_zotero_version)

        return []

    else:
        if from_version > last_zotero_version:
            # This should never happen, but just in case, we solve the error by syncing the penultimate version in Zotero
            from_version = last_zotero_version - 1
            print 'Error solved'

        print 'Getting items since version %d' % (from_version)
        print 'Last version in Zotero is %d' % (last_zotero_version)

        zot = get_zotero_connection()
        
        total_items = []
        
        #
        # 
        #           W A R N I N G            W A R N I N G        W A R N I N G
        # 
        # USE_CACHE is used for caching the results. It's useful for debugging, but should NEVER be true in production
        # 
        USE_CACHE = False
        CACHE_FILE = 'cache.pickle'
        if USE_CACHE and os.path.exists(CACHE_FILE):
            print "LOADING FROM CACHE!!!"
            items = pickle.load(open(CACHE_FILE))
        else:
            start = 0
            limit = 100
            items = zot.items(since=from_version, limit = limit, start = start)
            total_items.extend(items)
            while len(items) > 0:
                start += limit
                print "%s results found. Trying with ?start=%s" % (len(items), start)
                items = zot.items(since=from_version, limit = limit, start = start)
                if items:
                    print "Last paper added: %s" % (items[-1]['data']['dateAdded'])
                total_items.extend(items)

            items = total_items

            # Used for USE_CACHE. WARNING
            pickle.dump(items, open(CACHE_FILE,'w'))

        print
        print '*' * 50
        print '%d new items (includes attachments as items)' % len(items)
        print '*' * 50
        print
        
        items_ordered = {}
        attachments = []
        for item in items:
            if item['data']['itemType'] == 'attachment':
                if item['data']['filename'].lower().endswith(ACCEPTED_ATTACHMENT_FORMATS):
                    attachments.append(item)
                else:
                    print "Invalid attachment. File %s not ending with %s." % (item['data']['filename'], ACCEPTED_ATTACHMENT_FORMATS)
            else:
                item_id = item['key']
                items_ordered[item_id] = item
        
        attachment_number = 0

        for a in attachments:
            if 'parentItem' in a['data']:
                attachment_number += 1
                parent_id = a['data']['parentItem']
                if items_ordered.has_key(parent_id):
                    items_ordered[parent_id]['attachment'] = a
                else: 
                    #only the attachment has been modified
                    parent_publication = zot.item(parent_id)
                    publication_slug = slugify(parent_publication['data']['title'])
                    _save_attachment(a['key'], publication_slug, a['data']['filename'])
            else:
                print a['data'].get('title', 'The user did not even added a title'), "did not have a parentItem"
        
        number_of_items = len(items_ordered)
        print
        print '*' * 50
        print '%d items (%s attachments)' % (number_of_items, attachment_number)
        print '*' * 50
        print

        
        for pos, i_id in enumerate(items_ordered):
            item = items_ordered[i_id]
            publication_type = item['data']['itemType']
            print '\t[%s/%s][%s][%s] > %s' % (pos + 1, number_of_items, time.asctime(), publication_type.encode('utf-8'), item['data'].get('title','No title').encode('utf-8'))
            generate_publication(item)


####################################################################################################
# def: clean_database()
####################################################################################################

def clean_database():
    Publication.objects.all().delete()

    PublicationAuthor.objects.all().delete()
    PublicationEditor.objects.all().delete()
    PublicationTag.objects.all().delete()

    ZoteroExtractorLog.objects.all().delete()

####################################################################################################
# def: generate_publication_from_zotero()
####################################################################################################

def generate_publication(item):
    publication_type = item['data']['itemType']

    if publication_type == 'conferencePaper':
        parse_conference_paper(item)
    elif publication_type == 'bookSection':
        parse_book_section(item)
    elif publication_type == 'book':
        parse_authored_book(item)
    elif publication_type == 'journalArticle':
        parse_journal_article(item)
    elif publication_type == 'magazineArticle':
        parse_magazine_article(item)
    elif publication_type == 'attachment':
        pass # this should not happen
    elif publication_type == 'thesis':
        parse_thesis(item)
    else:
        print
        print '*' * 50
        print 'NOT PARSED:\t\tPublication type: %s' % publication_type
        print '*' * 50
        print
        pp.pprint(item)
        print
        
###############################################################################
###############################################################################
# Item parsing
###############################################################################
###############################################################################
        
####################################################################################################
# def: parse_journal_article()
####################################################################################################

def parse_journal_article(item):
    publication_slug = slugify(item['data']['title'])
    try:
        journal_article = JournalArticle.objects.get(slug=publication_slug)

    except ObjectDoesNotExist:
        journal_article = JournalArticle()

    journal_article.title = item['data']['title']
    journal_article.short_title = _extract_short_title(item)

    journal_article.abstract = _assign_if_exists(item, 'abstractNote')
    journal_article.pages = _assign_if_exists(item, 'pages')
    journal_article.doi = _extract_doi(item)

    journal_article.parent_journal = parse_journal(item)

    journal_article.published = _parse_date(item['data']['date'])
    journal_article.year = journal_article.published.year

    journal_article.bibtex = _extract_bibtex(item['key'])

    journal_article.save()

    _save_publication_authors(_extract_authors(item), journal_article)

    _extract_tags(item, journal_article)
    
    if item.has_key('attachment'):         
         _save_attachment(item['attachment']['key'], publication_slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, journal_article)     
    
    
####################################################################################################
# def: parse_journal()
####################################################################################################

def parse_journal(item):
    journal_slug = nslugify(item['data']['publicationTitle'], _parse_date(item['data']['date']).year, item['data'].get('volume'), item['data'].get('issue'))
    try:
        journal = Journal.objects.get(slug=journal_slug)
        
    except ObjectDoesNotExist:
        journal = Journal()

    journal.title = item['data']['publicationTitle']

    journal.issn = _assign_if_exists(item, 'ISSN')
    journal.volume = _assign_if_exists(item, 'volume')
    journal.publisher = _assign_if_exists(item, 'publisher')
    journal.place = _assign_if_exists(item, 'place')
    journal.journal_abbreviation = _assign_if_exists(item, 'journalAbbrevation')
    journal.issue = _assign_if_exists(item, 'issue')

    journal.published = _parse_date(item['data']['date'])
    journal.year = journal.published.year

    journal.save()

    return journal
    
####################################################################################################
# def: parse_conference_paper()
####################################################################################################

def parse_conference_paper(item):
    publication_slug = slugify(item['data']['title'])
    try:
        conference_paper = ConferencePaper.objects.get(slug=publication_slug)

    except ObjectDoesNotExist:
        conference_paper = ConferencePaper()

    conference_paper.title = item['data']['title']
    conference_paper.short_title = _extract_short_title(item)

    conference_paper.abstract = _assign_if_exists(item, 'abstractNote')
    conference_paper.pages = _assign_if_exists(item, 'pages')
    conference_paper.doi = _extract_doi(item)

    conference_paper.parent_proceedings = parse_proceedings(item)
    conference_paper.presented_at = parse_conference(item, conference_paper.parent_proceedings)

    conference_paper.published = _parse_date(item['data']['date'])
    conference_paper.year = conference_paper.published.year

    conference_paper.bibtex = _extract_bibtex(item['key'])

    conference_paper.save()

    _save_publication_authors(_extract_authors(item), conference_paper)

    _extract_tags(item, conference_paper)
    
    if 'attachment' in item:
        _save_attachment(item['attachment']['key'], publication_slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, conference_paper)


####################################################################################################
# def: parse_proceedings()
####################################################################################################

def parse_proceedings(item):
    if item['data']['proceedingsTitle'] != '':
        proceedings_title = item['data']['proceedingsTitle']

    else:
        if item['data']['conferenceName'] != '':
            proceedings_title = 'Proceedings of conference: %s' % item['data']['conferenceName']

        else:
            proceedings_title = 'Proceedings for article: %s' % item['data']['title']

    try:
        proceedings = Proceedings.objects.get(
            slug=nslugify(proceedings_title, _parse_date(item['data']['date']).year, item['data'].get('volume')),
            year=_parse_date(item['data']['date']).year
        )

    except ObjectDoesNotExist:
        proceedings = Proceedings()

    proceedings.title = proceedings_title

    proceedings.isbn = _assign_if_exists(item, 'ISBN')
    proceedings.volume = _assign_if_exists(item, 'volume')
    proceedings.series = _assign_if_exists(item, 'series')
    proceedings.publisher = _assign_if_exists(item, 'publisher')
    proceedings.place = _assign_if_exists(item, 'place')

    proceedings.published = _parse_date(item['data']['date'])
    proceedings.year = proceedings.published.year

    proceedings.save()

    return proceedings
    
####################################################################################################
# def: parse_conference()
####################################################################################################

def parse_conference(item, proceedings):
    if item['data'].has_key('conferenceName') and item['data']['conferenceName'] != '':
        try:
            event = Event.objects.get(
                slug=nslugify(item['data']['conferenceName'], _parse_date(item['data']['date']).year),
            )

        except ObjectDoesNotExist:
            event = Event()

        event.event_type = 'Academic event'

        event.full_name = item['data']['conferenceName']

        if  item['data'].has_key('place') and item['data']['place'] != '':
            places_list = item['data']['place'].split(', ')

            if len(places_list) == 2:
                city_name = places_list[0]
                country_name = places_list[1]

                event_location = ''

                if city_name and city_name != '':
                    try:
                        city = City.objects.get(slug=slugify(city_name))

                    except ObjectDoesNotExist:
                        city = City(
                            full_name=city_name,
                        )

                        city.save()

                    event_location = city_name

                else:
                    city = None

                if country_name and country_name != '':
                    try:
                        country = Country.objects.get(slug=slugify(country_name))

                    except ObjectDoesNotExist:
                        country = Country(
                            full_name=country_name,
                        )

                        country.save()

                    city.country = country
                    city.save()

                    if city_name and city_name != '':
                        event_location = '%s (%s)' % (event_location, country_name)
                    else:
                        event_location = '(%s)' % country_name

                else:
                    country = None

                event.host_city = city
                event.host_country = country

                event.location = event_location

        event.start_date = _parse_date(item['data']['date'])
        event.year = event.start_date.year

        event.proceedings = proceedings

        event.save()

        return event

    else:
        return None
        
####################################################################################################
# def: parse_book_section()
####################################################################################################

def parse_book_section(item):
    publication_slug = slugify(item['data']['title'])
    try:
        book_section = BookSection.objects.get(slug=publication_slug)

    except ObjectDoesNotExist:
        book_section = BookSection()

    book_section.title = item['data']['title']
    book_section.short_title = _extract_short_title(item)

    book_section.abstract = _assign_if_exists(item, 'abstractNote')
    book_section.pages = _assign_if_exists(item, 'pages')
    book_section.doi = _extract_doi(item)

    book_section.parent_book = parse_book(item)

    book_section.published = _parse_date(item['data']['date'])
    book_section.year = book_section.published.year

    book_section.bibtex = _extract_bibtex(item['key'])

    book_section.save()

    _save_publication_authors(_extract_authors(item), book_section)

    _extract_tags(item, book_section)
    
    if item.has_key('attachment'):         
         _save_attachment(item['attachment']['key'], publication_slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, book_section)


####################################################################################################
# def: parse_book()
####################################################################################################

def parse_book(item):
    try:
        book = Book.objects.get(
            slug=nslugify(item['data']['bookTitle'], _parse_date(item['data']['date']).year, item['data'].get('volume'), item['data'].get('series')),
            year=_parse_date(item['data']['date']).year
        )

    except ObjectDoesNotExist:
        book = Book()

    book.title = item['data']['bookTitle']

    book.isbn = _assign_if_exists(item, 'ISBN')
    book.volume = _assign_if_exists(item, 'volume')
    book.series = _assign_if_exists(item, 'series')
    book.publisher = _assign_if_exists(item, 'publisher')
    book.place = _assign_if_exists(item, 'place')

    book.published = _parse_date(item['data']['date'])
    book.year = book.published.year

    book.save()

    _save_publication_editors(_extract_editors(item), book)

    return book
    
####################################################################################################
# def: parse_authored_book()
####################################################################################################

def parse_authored_book(item):
    publication_slug = nslugify(item['data']['title'], _parse_date(item['data']['date']).year, item['data']['volume'], item['data']['series'])
    try:
        book = Book.objects.get(slug=publication_slug)

    except ObjectDoesNotExist:
        book = Book()

    book.title = item['data']['title']
    book.short_title = _extract_short_title(item)

    book.abstract = _assign_if_exists(item, 'abstractNote')
    book.number_of_pages = _assign_if_exists(item, 'numPages')
    book.edition = _assign_if_exists(item, 'edition')
    book.doi = _extract_doi(item)

    book.isbn = _assign_if_exists(item, 'ISBN')
    book.volume = _assign_if_exists(item, 'volume')
    book.number_of_volumes = _assign_if_exists(item, 'numberOfVolumes')
    book.series = _assign_if_exists(item, 'series')
    book.series_number = _assign_if_exists(item, 'seriesNumber')
    book.publisher = _assign_if_exists(item, 'publisher')
    book.place = _assign_if_exists(item, 'place')

    book.published = _parse_date(item['data']['date'])
    book.year = book.published.year

    book.bibtex = _extract_bibtex(item['key'])

    book.save()

    _save_publication_authors(_extract_authors(item), book)

    _extract_tags(item, book)
    
    if item.has_key('attachment'):         
         _save_attachment(item['attachment']['key'], publication_slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, book)
    
####################################################################################################
# def: parse_magazine_article()
####################################################################################################

def parse_magazine_article(item):
    publication_slug = slugify(item['data']['title'])
    try:
        magazine_article = MagazineArticle.objects.get(slug=publication_slug)

    except ObjectDoesNotExist:
        magazine_article = MagazineArticle()

    magazine_article.title = item['data']['title']
    magazine_article.short_title = _extract_short_title(item)

    magazine_article.abstract = _assign_if_exists(item, 'abstractNote')
    magazine_article.pages = _assign_if_exists(item, 'pages')
    magazine_article.doi = _extract_doi(item)

    magazine_article.parent_magazine = parse_magazine(item)

    magazine_article.published = _parse_date(item['data']['date'])
    magazine_article.year = magazine_article.published.year

    magazine_article.bibtex = _extract_bibtex(item['key'])

    magazine_article.save()

    _save_publication_authors(_extract_authors(item), magazine_article)

    _extract_tags(item, magazine_article)
    
    if item.has_key('attachment'):         
         _save_attachment(item['attachment']['key'], publication_slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, magazine_article)


####################################################################################################
# def: parse_magazine()
####################################################################################################

def parse_magazine(item):
    try:
        magazine = Magazine.objects.get(
            slug=nslugify(item['data']['publicationTitle'], _parse_date(item['data']['date']).year, item['data'].get('volume'), item['data'].get('issue')),
            year=_parse_date(item['data']['date']).year
        )

    except ObjectDoesNotExist:
        magazine = Magazine()

    magazine.title = item['data']['publicationTitle']

    magazine.issn = _assign_if_exists(item, 'ISSN')
    magazine.volume = _assign_if_exists(item, 'volume')
    magazine.issue = _assign_if_exists(item, 'issue')

    magazine.published = _parse_date(item['data']['date'])
    magazine.year = magazine.published.year

    magazine.save()

    return magazine





####################################################################################################
# def: parse_thesis()
####################################################################################################

def parse_thesis(item):
    author = _extract_authors(item)[0]

    try:
        Thesis.objects.get(slug=slugify(item['data']['title']))

    except ObjectDoesNotExist:
        print
        print '*' * 75
        print '%s should register his/her thesis using labman\'s admin page' % author
        print '*' * 75
        print

###############################################################################
###############################################################################
# Common methods
###############################################################################
###############################################################################
        
####################################################################################################
# def: _extract_short_title()
####################################################################################################

def _extract_short_title(item):
    if item['data'].get('shortTitle'):
        return item['data']['shortTitle']
    else:
        index = item['data']['title'].find(':')

        if index != -1:
            return item['data']['title'][:index]        
        
####################################################################################################
# def: _assign_if_exists()
####################################################################################################

def _assign_if_exists(item, key):
    if item['data'].get(key):
        return item['data'][key]
            
####################################################################################################
# def: _extract_doi()
####################################################################################################

def _extract_doi(item):
    DOI_ORG_BASE_URL = 'http://dx.doi.org/'

    if item['data'].has_key('DOI'):
        if item['data']['DOI'] != '':
            return item['data']['DOI']

    elif item['data'].has_key('url'):
        if item['data']['url'] != '' and DOI_ORG_BASE_URL in item['data']['url']:
            base_url_end_index = len(DOI_ORG_BASE_URL)
            underscore_index = item['data']['url'].find('_') if item['data']['url'].find('_') != -1 else len(item['data']['url'])

            return item['data']['url'][base_url_end_index:underscore_index]
        
####################################################################################################
# def: _parse_date()
####################################################################################################

def _parse_date(date_string): 
    return parser.parse(date_string, fuzzy=True, default=datetime.now())   

####################################################################################################
# def: _extract_bibtex()
####################################################################################################

def _extract_bibtex(item_key):
    zot = get_zotero_connection()

    counter = 4
    while counter >= 0:
        counter -= 1
        try:
            item = zot.item(item_key, format='bibtex')
        except (HTTPError, socket.error) as e:
            print "Error %s. Retrying in 5 seconds" % e
            time.sleep(5)
            if counter == 0:
                raise
        else:
            break

    return item
    
####################################################################################################
# def: _extract_authors()
####################################################################################################

def _extract_authors(item):
    authors = []

    if  item['data'].has_key('creators') and len(item['data']['creators']) > 0:
        for creator_item in item['data']['creators']:
            creator_type = creator_item['creatorType']

            if creator_type == 'author':
                if 'name' in creator_item and creator_item['name'] != '':
                    author_name = str(creator_item['name'].encode('utf-8'))
                    author_first_surname = author_name.split(' ')[-1]
                    author_first_name = author_name.replace(' ' + author_first_surname, '')

                else:
                    author_first_name = creator_item['firstName'].encode('utf-8')
                    author_first_surname = creator_item['lastName'].encode('utf-8')

                author_slug = slugify('%s %s' % (author_first_name, author_first_surname))

                try:
                    # Check if author is in DB (comparing by slug)
                    author = Person.objects.get(slug=author_slug)

                except ObjectDoesNotExist:
                    # If it isn't
                    # Check if author name correspond with any of the posible nicknames of the authors in DB
                    nicks = Nickname.objects.filter(slug=author_slug).all()
                    if nicks:
                        author = nicks[0].person
                    else:
                        # If there is no reference to that person in the DB, create a new one
                        author = Person(
                            first_name=author_first_name,
                            first_surname=author_first_surname
                        )

                        author.save()

                authors.append(author)

    return authors
    
####################################################################################################
# def: _save_publication_authors()
####################################################################################################

def _save_publication_authors(authors, publication):
    order = 1

    existing_authors = PublicationAuthor.objects.filter(publication = publication).all()
    for existing_author in existing_authors:
        existing_author.delete()

    for author in authors:
        publication_author = PublicationAuthor(
            author=author,
            publication=publication,
            position=order,
        )

        publication_author.save()

        order += 1               
        
####################################################################################################
# def: _extract_tags()
####################################################################################################

def _extract_tags(item, publication):

    # Clean ranking and projects so as to ensure that it's correctly synchronized
    existing_rankings = PublicationRank.objects.filter(publication = publication).all()
    for existing_ranking in existing_rankings:
        existing_ranking.delete()

    existing_projects = RelatedPublication.objects.filter(publication = publication).all()
    for existing_project in existing_projects:
        existing_project.delete()

    existing_tags = PublicationTag.objects.filter(publication = publication).all()
    for existing_tag in existing_tags:
        existing_tag.delete()

    if item['data'].has_key('tags') and len(item['data']['tags']) > 0:
        for tag_item in item['data']['tags']:
            tag_name = tag_item['tag'].encode('utf-8')

            if _determine_if_tag_is_special(tag_name, publication):
                pass

            else:
                try:
                    tag = Tag.objects.get(slug=slugify(tag_name))

                except ObjectDoesNotExist:
                    tag = Tag(
                        name=tag_name,
                    )

                    tag.save()

                publication_tag = PublicationTag(
                    tag=tag,
                    publication=publication,
                )

                publication_tag.save()        
        
####################################################################################################
# def: _save_zotero_extractor_log()
####################################################################################################

def _save_zotero_extractor_log(item, publication):
    zotero_extractor_log = ZoteroExtractorLog(
        item_key=item['key'],
        version=item['version'],
        publication=publication,
    )

    zotero_extractor_log.save()
        
        
####################################################################################################
# def: _save_attachment()
####################################################################################################

def _save_attachment(attachment_id, publication_slug, filename):
    zot = get_zotero_connection()
    counter = 4
    while counter >= 0:
        counter -= 1
        try:
            item = zot.file(attachment_id)
        except (HTTPError, socket.error) as e:
            print "Error %s. Retrying in 5 seconds" % e
            time.sleep(5)
            if counter == 0:
                raise
        else:
            break

    publication = Publication.objects.get(slug=publication_slug)
    path = publication_path(publication, filename)

    # If the directory doesn't exist, create it
    pdf_dir = getattr(settings, 'MEDIA_ROOT', None) + '/' + os.path.dirname(path)

    if not os.path.exists(pdf_dir):
        os.makedirs(pdf_dir)

    with open(getattr(settings, 'MEDIA_ROOT', None) + '/' + path, 'wb') as pdffile:
        pdffile.write(item)

    publication.pdf = path
    publication.save() 
    
####################################################################################################
# def: _extract_editors()
####################################################################################################

def _extract_editors(item):
    editors = []

    if item['data'].has_key('creators') and len(item['data']['creators']) > 0:
        for creator_item in item['data']['creators']:
            creator_type = creator_item['creatorType']

            if creator_type == 'editor':
                if 'name' in creator_item and creator_item['name'] != '':
                    editor_name = str(creator_item['name'].encode('utf-8'))
                    editor_first_surname = editor_name.split(' ')[-1]
                    editor_first_name = editor_name.replace(' ' + editor_first_surname, '')

                else:
                    editor_first_name = creator_item['firstName'].encode('utf-8')
                    editor_first_surname = creator_item['lastName'].encode('utf-8')

                editor_slug = slugify('%s %s' % (editor_first_name, editor_first_surname))

                try:
                    # Check if editor is in DB (comparing by slug)
                    editor = Person.objects.get(slug=editor_slug)

                except ObjectDoesNotExist:
                    # If it isn't
                    try:
                        # Check if editor name correspond with any of the posible nicknames of the authors in DB
                        nick = Nickname.objects.get(slug=editor_slug)
                        editor = nick.person
                    except ObjectDoesNotExist:
                        # If there is no reference to that person in the DB, create a new one
                        editor = Person(
                            first_name=editor_first_name,
                            first_surname=editor_first_surname
                        )

                        editor.save()

                editors.append(editor)

    return editors
    
####################################################################################################
# def: _save_publication_editors()
####################################################################################################

def _save_publication_editors(editors, publication):
    existing_editors = PublicationEditor.objects.filter(publication=publication).all()
    for existing_editor in existing_editors:
        existing_editor.delete()

    for editor in editors:
        publication_editor = PublicationEditor(
            editor=editor,
            publication=publication,
        )

        publication_editor.save()
        
####################################################################################################
# def: _determine_if_tag_is_special()
####################################################################################################

def _determine_if_tag_is_special(tag, publication):
    tag_slug = slugify(tag)
    jcr_match = re.match(JCR_PATTERN, tag.lower())

    project_slugs = Project.objects.all().values_list('slug', flat=True)
    ranking_slugs = Ranking.objects.all().values_list('slug', flat=True)

    special = True

    if tag_slug in ranking_slugs:
        ranking = Ranking.objects.get(slug=tag_slug)
        publication_ranking = PublicationRank(ranking = ranking, publication = publication)
        publication_ranking.save()

    elif (tag_slug in ['q1', 'q-1']) and (publication.child_type == 'JournalArticle'):
        publication.parent_journal.quartile = QUARTILE_CHOICES[0][0]
        publication.parent_journal.save()

    elif (tag_slug in ['q2', 'q-2']) and (publication.child_type == 'JournalArticle'):
        publication.parent_journal.quartile = QUARTILE_CHOICES[1][0]
        publication.parent_journal.save()

    elif (tag_slug in ['q3', 'q-3']) and (publication.child_type == 'JournalArticle'):
        publication.parent_journal.quartile = QUARTILE_CHOICES[3][0]
        publication.parent_journal.save()

    elif (tag_slug in ['q4', 'q-4']) and (publication.child_type == 'JournalArticle'):
        publication.parent_journal.quartile = QUARTILE_CHOICES[3][0]
        publication.parent_journal.save()

    elif (jcr_match) and (publication.child_type == 'JournalArticle'):
        tag_lower = tag.lower().replace(',', '.')
        non_decimal = re.compile(r'[^\d.]+')

        impact_factor = non_decimal.sub('', tag_lower)

        publication.parent_journal.impact_factor = float(impact_factor)
        publication.parent_journal.save()

    elif tag_slug in project_slugs:
        project = Project.objects.get(slug=tag_slug)

        related_publication = RelatedPublication(
            project=project,
            publication=publication,
        )

        related_publication.save()

    else:
        special = False

    return special

        
