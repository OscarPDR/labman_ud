# -*- coding: utf-8 -*-

from django.conf import settings
from django.db.models import Max
from django.template.defaultfilters import slugify

from entities.events.models import Event
from entities.persons.models import Person, Nickname
from entities.projects.models import Project, RelatedPublication
from entities.publications.models import *
from entities.utils.models import Tag, City, Country
from extractors.zotero.models import ZoteroExtractorLog

from datetime import datetime
from dateutil import parser
from xml.dom import minidom

import json
import operator
import os
import pprint
import re
import requests

pp = pprint.PrettyPrinter(indent=4)

JCR_PATTERN = r'(jcr|if)(-*)(\d(\.|\,)\d+)'


####################################################################################################
# def: get_zotero_variables()
####################################################################################################

def get_zotero_variables():
    base_url = getattr(settings, 'ZOTERO_API_BASE_URL', None)
    api_key = getattr(settings, 'ZOTERO_API_KEY', None)
    library_id = getattr(settings, 'ZOTERO_LIBRARY_ID', None)
    library_type = getattr(settings, 'ZOTERO_LIBRARY_TYPE', None)

    return base_url, api_key, library_id, library_type


####################################################################################################
# def: _get_last_zotero_version()
####################################################################################################

def _get_last_zotero_version():
    base_url, api_key, library_id, library_type = get_zotero_variables()

    url = '%s/%ss/%s/items' % (base_url, library_type, library_id)

    headers = {'Zotero-API-Version': 2}

    params = {
        'key': api_key,
        'format': 'versions',
    }

    r = requests.get(url, headers=headers, params=params)

    if len(r.json()):
        latest_version_number = max(r.json().items(), key=operator.itemgetter(1))[1]
    else:
        latest_version_number = 0

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

def get_item_keys_since_last_synchronized_version(from_version):
    last_zotero_version = _get_last_zotero_version()

    if from_version == last_zotero_version:
        print 'Labman is updated to the last version in Zotero (%d)' % (last_zotero_version)

        return []

    else:
        if from_version > last_zotero_version:
            # This should never happen, but just in case, we solve the error by syncing the penultimate version in Zotero
            print 'Labman version number (%d) is higher than Zotero\'s one (%d)...' % (version, last_version)
            from_version = last_zotero_version - 1
            print 'Error solved'

        print 'Getting items since version %d' % (from_version)
        print 'Last version in Zotero is %d' % (last_zotero_version)

        base_url, api_key, library_id, library_type = get_zotero_variables()

        url = '%s/%ss/%s/items' % (base_url, library_type, library_id)

        headers = {'Zotero-API-Version': 2}

        params = {
            'key': api_key,
            'format': 'keys',
            'order': 'dateModified',
            'sort': 'desc',
            'newer': from_version,
            'limit': 10000,
        }

        r = requests.get(url, headers=headers, params=params)

        item_key_list = r.text.split('\n')

        while '' in item_key_list:
            item_key_list.remove('')

        return item_key_list


####################################################################################################
# def: clean_database()
####################################################################################################

def clean_database():
    Publication.objects.all().delete()

    PublicationAuthor.objects.all().delete()
    PublicationEditor.objects.all().delete()
    PublicationTag.objects.all().delete()

    ZoteroExtractorLog.objects.all().delete()

    Event.objects.filter(event_type__name='Academic event').delete()
    City.objects.all().delete()


####################################################################################################
# def: extract_publications_from_zotero()
####################################################################################################

def extract_publications_from_zotero(from_version):
    item_key_list = get_item_keys_since_last_synchronized_version(from_version)

    print
    print '*' * 50
    print '%d new items' % len(item_key_list)
    print '*' * 50
    print

    for item_key in item_key_list:
        try:
            generate_publication_from_zotero(item_key)

        except:
            print 'Error retrieving information from Zotero API about item: %s' % item_key


####################################################################################################
# def: generate_publication_from_zotero()
####################################################################################################

def generate_publication_from_zotero(item_key):
    base_url, api_key, library_id, library_type = get_zotero_variables()

    url = '%s/%ss/%s/items/%s' % (base_url, library_type, library_id, item_key)

    headers = {'Zotero-API-Version': 2}

    params = {
        'key': api_key,
        'content': 'json',
    }

    r = requests.get(url, headers=headers, params=params)
    print r.url

    xmldoc = minidom.parseString(r.text.encode('utf-8').replace("'", ""))
    content = xmldoc.getElementsByTagName('content')[0].firstChild.nodeValue
    content_json = json.loads(content)

    publication_type = content_json['itemType']

    print '\t[%s] > %s' % (publication_type.encode('utf-8'), content_json['title'].encode('utf-8'))

    if publication_type == 'conferencePaper':
        parse_conference_paper(content_json, item_key)
    elif publication_type == 'bookSection':
        parse_book_section(content_json, item_key)
    elif publication_type == 'book':
        parse_authored_book(content_json, item_key)
    elif publication_type == 'journalArticle':
        parse_journal_article(content_json, item_key)
    elif publication_type == 'magazineArticle':
        parse_magazine_article(content_json, item_key)
    elif publication_type == 'attachment':
        pass
    elif publication_type == 'thesis':
        parse_thesis(content_json)
    else:
        print
        print '*' * 50
        print 'NOT PARSED:\t\tPublication type: %s' % publication_type
        print '*' * 50
        print
        pp.pprint(content_json)
        print

    if publication_type in ['conferencePaper', 'bookSection', 'book', 'journalArticle', 'magazineArticle']:
        try:
            number_of_children = int(xmldoc.getElementsByTagName('zapi:numChildren')[0].firstChild.nodeValue)

        except:
            number_of_children = 0

        if number_of_children > 0:
            parse_attachment(item_key, publication_type)


####################################################################################################
# def: parse_conference_paper()
####################################################################################################

def parse_conference_paper(json_item, item_key):
    try:
        conference_paper = ConferencePaper.objects.get(slug=slugify(json_item['title']))

    except:
        conference_paper = ConferencePaper()

        conference_paper.title = json_item['title']
        conference_paper.short_title = _extract_short_title(json_item)

        conference_paper.abstract = _assign_if_exists(json_item, 'abstractNote')
        conference_paper.pages = _assign_if_exists(json_item, 'pages')
        conference_paper.doi = _extract_doi(json_item)

        conference_paper.parent_proceedings = parse_proceedings(json_item)
        conference_paper.presented_at = parse_conference(json_item, conference_paper.parent_proceedings)

        conference_paper.published = _parse_date(json_item['date'])
        conference_paper.year = conference_paper.published.year

        conference_paper.bibtex = _extract_bibtex(item_key)

        conference_paper.save()

    _save_publication_authors(_extract_authors(json_item), conference_paper)

    _extract_tags(json_item, conference_paper)

    _save_zotero_extractor_log(json_item, conference_paper)


####################################################################################################
# def: parse_proceedings()
####################################################################################################

def parse_proceedings(json_item):
    if json_item['proceedingsTitle'] != '':
        proceedings_title = json_item['proceedingsTitle']

    else:
        if json_item['conferenceName'] != '':
            proceedings_title = 'Proceedings of conference: %s' % json_item['conferenceName']

        else:
            proceedings_title = 'Proceedings for article: %s' % json_item['title']

    try:
        proceedings = Proceedings.objects.get(slug=slugify(proceedings_title))

    except:
        proceedings = Proceedings()

        proceedings.title = proceedings_title

        proceedings.isbn = _assign_if_exists(json_item, 'ISBN')
        proceedings.volume = _assign_if_exists(json_item, 'volume')
        proceedings.series = _assign_if_exists(json_item, 'series')
        proceedings.publisher = _assign_if_exists(json_item, 'publisher')
        proceedings.place = _assign_if_exists(json_item, 'place')

        proceedings.published = _parse_date(json_item['date'])
        proceedings.year = proceedings.published.year

        proceedings.save()

    return proceedings


####################################################################################################
# def: parse_conference()
####################################################################################################

def parse_conference(json_item, proceedings):
    if 'conferenceName' in json_item.keys() and json_item['conferenceName'] != '':
        try:
            event = Event.objects.get(slug=slugify(json_item['conferenceName']))

        except:
            event = Event()

        event.event_type = 'Academic event'

        event.full_name = json_item['conferenceName']

        if 'place' in json_item.keys() and json_item['place'] != '':
            places_list = json_item['place'].split(', ')

            if len(places_list) == 2:
                city_name = places_list[0]
                country_name = places_list[1]

                event_location = ''

                if city_name and city_name != '':
                    try:
                        city = City.objects.get(slug=slugify(city_name))

                    except:
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

                    except:
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

        event.published = _parse_date(json_item['date'])
        event.year = event.published.year

        event.proceedings = proceedings

        event.save()

        return event

    else:
        return None


####################################################################################################
# def: parse_book_section()
####################################################################################################

def parse_book_section(json_item, item_key):
    try:
        book_section = BookSection.objects.get(slug=slugify(json_item['title']))

    except:
        book_section = BookSection()

        book_section.title = json_item['title']
        book_section.short_title = _extract_short_title(json_item)

        book_section.abstract = _assign_if_exists(json_item, 'abstractNote')
        book_section.pages = _assign_if_exists(json_item, 'pages')
        book_section.doi = _extract_doi(json_item)

        book_section.parent_book = parse_book(json_item)

        book_section.published = _parse_date(json_item['date'])
        book_section.year = book_section.published.year

        book_section.bibtex = _extract_bibtex(item_key)

        book_section.save()

    _save_publication_authors(_extract_authors(json_item), book_section)

    _extract_tags(json_item, book_section)

    _save_zotero_extractor_log(json_item, book_section)


####################################################################################################
# def: parse_book()
####################################################################################################

def parse_book(json_item):
    try:
        book = Book.objects.get(slug=slugify(json_item['bookTitle']))

    except:
        book = Book()

        book.title = json_item['bookTitle']

        book.isbn = _assign_if_exists(json_item, 'ISBN')
        book.volume = _assign_if_exists(json_item, 'volume')
        book.series = _assign_if_exists(json_item, 'series')
        book.publisher = _assign_if_exists(json_item, 'publisher')
        book.place = _assign_if_exists(json_item, 'place')

        book.published = _parse_date(json_item['date'])
        book.year = book.published.year

        book.save()

    _save_publication_editors(_extract_editors(json_item), book)

    return book


####################################################################################################
# def: parse_authored_book()
####################################################################################################

def parse_authored_book(json_item, item_key):
    try:
        book = Book.objects.get(slug=slugify(json_item['title']))

    except:
        book = Book()

        book.title = json_item['title']
        book.short_title = _extract_short_title(json_item)

        book.abstract = _assign_if_exists(json_item, 'abstractNote')
        book.number_of_pages = _assign_if_exists(json_item, 'numPages')
        book.edition = _assign_if_exists(json_item, 'edition')
        book.doi = _extract_doi(json_item)

        book.isbn = _assign_if_exists(json_item, 'ISBN')
        book.volume = _assign_if_exists(json_item, 'volume')
        book.number_of_volumes = _assign_if_exists(json_item, 'numberOfVolumes')
        book.series = _assign_if_exists(json_item, 'series')
        book.series_number = _assign_if_exists(json_item, 'seriesNumber')
        book.publisher = _assign_if_exists(json_item, 'publisher')
        book.place = _assign_if_exists(json_item, 'place')

        book.published = _parse_date(json_item['date'])
        book.year = book.published.year

        book.bibtex = _extract_bibtex(item_key)

        book.save()

    _save_publication_authors(_extract_authors(json_item), book)

    _extract_tags(json_item, book)

    _save_zotero_extractor_log(json_item, book)


####################################################################################################
# def: parse_journal_article()
####################################################################################################

def parse_journal_article(json_item, item_key):
    try:
        journal_article = JournalArticle.objects.get(slug=slugify(json_item['title']))

    except:
        journal_article = JournalArticle()

        journal_article.title = json_item['title']
        journal_article.short_title = _extract_short_title(json_item)

        journal_article.abstract = _assign_if_exists(json_item, 'abstractNote')
        journal_article.pages = _assign_if_exists(json_item, 'pages')
        journal_article.doi = _extract_doi(json_item)

        journal_article.parent_journal = parse_journal(json_item)

        journal_article.published = _parse_date(json_item['date'])
        journal_article.year = journal_article.published.year

        journal_article.bibtex = _extract_bibtex(item_key)

        journal_article.save()

    _save_publication_authors(_extract_authors(json_item), journal_article)

    _extract_tags(json_item, journal_article)

    _save_zotero_extractor_log(json_item, journal_article)


####################################################################################################
# def: parse_journal()
####################################################################################################

def parse_journal(json_item):
    try:
        journal = Journal.objects.get(slug=slugify(json_item['publicationTitle']))

    except:
        journal = Journal()

        journal.title = json_item['publicationTitle']

        journal.issn = _assign_if_exists(json_item, 'ISSN')
        journal.volume = _assign_if_exists(json_item, 'volume')
        journal.series = _assign_if_exists(json_item, 'series')
        journal.publisher = _assign_if_exists(json_item, 'publisher')
        journal.place = _assign_if_exists(json_item, 'place')
        journal.journal_abbreviation = _assign_if_exists(json_item, 'journalAbbrevation')

        journal.published = _parse_date(json_item['date'])
        journal.year = journal.published.year

        journal.save()

    return journal


####################################################################################################
# def: parse_magazine_article()
####################################################################################################

def parse_magazine_article(json_item, item_key):
    try:
        magazine_article = MagazineArticle.objects.get(slug=slugify(json_item['title']))

    except:
        magazine_article = MagazineArticle()

        magazine_article.title = json_item['title']
        magazine_article.short_title = _extract_short_title(json_item)

        magazine_article.abstract = _assign_if_exists(json_item, 'abstractNote')
        magazine_article.pages = _assign_if_exists(json_item, 'pages')
        magazine_article.doi = _extract_doi(json_item)

        magazine_article.parent_magazine = parse_magazine(json_item)

        magazine_article.published = _parse_date(json_item['date'])
        magazine_article.year = magazine_article.published.year

        magazine_article.bibtex = _extract_bibtex(item_key)

        magazine_article.save()

    _save_publication_authors(_extract_authors(json_item), magazine_article)

    _extract_tags(json_item, magazine_article)

    _save_zotero_extractor_log(json_item, magazine_article)


####################################################################################################
# def: parse_magazine()
####################################################################################################

def parse_magazine(json_item):
    try:
        magazine = Magazine.objects.get(slug=slugify(json_item['publicationTitle']))

    except:
        magazine = Magazine()

        magazine.title = json_item['publicationTitle']

        magazine.issn = _assign_if_exists(json_item, 'ISSN')
        magazine.volume = _assign_if_exists(json_item, 'volume')
        magazine.issue = _assign_if_exists(json_item, 'issue')

        magazine.published = _parse_date(json_item['date'])
        magazine.year = magazine.published.year

        magazine.save()

    return magazine


####################################################################################################
# def: parse_attachment()
####################################################################################################

def parse_attachment(item_key, publication_type):
    base_url, api_key, library_id, library_type = get_zotero_variables()

    url = '%s/%ss/%s/items/%s/children' % (base_url, library_type, library_id, item_key)

    headers = {'Zotero-API-Version': 2}

    params = {
        'key': api_key,
        'content': 'json',
    }

    r = requests.get(url, headers=headers, params=params)

    xmldoc = minidom.parseString(r.text.encode('utf-8').replace("'", ""))

    contents = xmldoc.getElementsByTagName('content')

    for content_item in contents:
        content = content_item.firstChild.nodeValue
        content_json = json.loads(content)

        if content_json['contentType'] == 'application/pdf':
            file_item_key = content_json['itemKey']

            base_url, api_key, library_id, library_type = get_zotero_variables()

            url = '%s/%ss/%s/items/%s/file' % (base_url, library_type, library_id, file_item_key)

            headers = {'Zotero-API-Version': 2}

            params = {
                'key': api_key,
            }

            r = requests.get(url, headers=headers, params=params)

            zotero_extractor_log = ZoteroExtractorLog.objects.filter(item_key=item_key).order_by('-timestamp')[0]
            publication = Publication.objects.get(pk=zotero_extractor_log.publication.id)

            path = publication_path(publication, content_json['filename'])

            # If the directory doesn't exist, create it
            pdf_dir = getattr(settings, 'MEDIA_ROOT', None) + '/' + os.path.dirname(path)

            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)

            with open(getattr(settings, 'MEDIA_ROOT', None) + '/' + path, 'wb') as pdffile:
                pdffile.write(r.content)

            publication.pdf = path

            publication.save()


####################################################################################################
# def: parse_thesis()
####################################################################################################

def parse_thesis(json_item):
    author = _extract_authors(json_item)[0]

    try:
        Thesis.objects.get(slug=slugify(json_item['title']))

    except:
        print
        print '*' * 75
        print '%s should register his/her thesis using labman\'s admin page' % author
        print '*' * 75
        print


####################################################################################################
# def: _parse_date()
####################################################################################################

def _parse_date(date_string):
    return parser.parse(date_string, fuzzy=True, default=datetime(2005, 1, 1))


####################################################################################################
# def: _assign_if_exists()
####################################################################################################

def _assign_if_exists(item, key):
    if key in item.keys():
        if item[key] != '':
            return item[key]


####################################################################################################
# def: _extract_doi()
####################################################################################################

def _extract_doi(item):
    DOI_ORG_BASE_URL = 'http://dx.doi.org/'

    if 'DOI' in item.keys():
        if item['DOI'] != '':
            return item['DOI']

    elif 'url' in item.keys():
        if item['url'] != '' and DOI_ORG_BASE_URL in item['url']:
            base_url_end_index = len(DOI_ORG_BASE_URL)
            underscore_index = item['url'].find('_') if item['url'].find('_') != -1 else len(item['url'])

            return item['url'][base_url_end_index:underscore_index]


####################################################################################################
# def: _extract_bibtex()
####################################################################################################

def _extract_bibtex(item_key):
    base_url, api_key, library_id, library_type = get_zotero_variables()

    url = '%s/%ss/%s/items/%s' % (base_url, library_type, library_id, item_key)

    headers = {'Zotero-API-Version': 2}

    params = {
        'key': api_key,
        'format': 'bibtex',
    }

    r = requests.get(url, headers=headers, params=params)

    return r.text.encode('utf-8')[1:]


####################################################################################################
# def: _extract_short_title()
####################################################################################################

def _extract_short_title(item):
    if 'shortTitle' in item.keys() and item['shortTitle'] != '':
        return item['shortTitle']

    else:
        index = item['title'].find(':')

        if index != -1:
            return item['title'][:index]


####################################################################################################
# def: _extract_authors()
####################################################################################################

def _extract_authors(item):
    authors = []

    if 'creators' in item.keys() and len(item['creators']) > 0:
        for creator_item in item['creators']:
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

                except:
                    # If it isn't
                    try:
                        # Check if author name correspond with any of the posible nicknames of the authors in DB
                        nick = Nickname.objects.get(slug=author_slug)
                        author = nick.person
                    except:
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

    for author in authors:
        publication_author = PublicationAuthor(
            author=author,
            publication=publication,
            position=order,
        )

        publication_author.save()

        order += 1


####################################################################################################
# def: _extract_editors()
####################################################################################################

def _extract_editors(item):
    editors = []

    if 'creators' in item.keys() and len(item['creators']) > 0:
        for creator_item in item['creators']:
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

                except:
                    # If it isn't
                    try:
                        # Check if editor name correspond with any of the posible nicknames of the authors in DB
                        nick = Nickname.objects.get(slug=editor_slug)
                        editor = nick.person
                    except:
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
    for editor in editors:
        publication_editor = PublicationEditor(
            editor=editor,
            publication=publication,
        )

        publication_editor.save()


####################################################################################################
# def: _extract_tags()
####################################################################################################

def _extract_tags(item, publication):
    if 'tags' in item.keys() and len(item['tags']) > 0:
        for tag_item in item['tags']:
            tag_name = tag_item['tag'].encode('utf-8')

            if _determine_if_tag_is_special(tag_name, publication):
                pass

            else:
                try:
                    tag = Tag.objects.get(slug=slugify(tag_name))

                except:
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
# def: _determine_if_tag_is_special()
####################################################################################################

def _determine_if_tag_is_special(tag, publication):
    tag_slug = slugify(tag)
    jcr_match = re.match(JCR_PATTERN, tag.lower())

    project_slugs = Project.objects.all().values_list('slug', flat=True)

    special = True

    if (tag_slug == 'isi') and (publication.child_type in ['ConferencePaper', 'BookSection', 'JournalArticle']):
        publication.isi = True
        publication.save()

    elif (tag_slug == 'dblp') and (publication.child_type in ['ConferencePaper', 'BookSection', 'JournalArticle']):
        publication.dblp = True
        publication.save()

    elif (tag_slug in ['corea', 'core-a']) and (publication.child_type in ['ConferencePaper', 'BookSection']):
        publication.core = CORE_CHOICES[0][0]
        publication.save()

    elif (tag_slug in ['coreb', 'core-b']) and (publication.child_type in ['ConferencePaper', 'BookSection']):
        publication.core = CORE_CHOICES[1][0]
        publication.save()

    elif (tag_slug in ['corec', 'core-c']) and (publication.child_type in ['ConferencePaper', 'BookSection']):
        publication.core = CORE_CHOICES[2][0]
        publication.save()

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


####################################################################################################
# def: _save_zotero_extractor_log()
####################################################################################################

def _save_zotero_extractor_log(item, publication):
    zotero_extractor_log = ZoteroExtractorLog(
        item_key=item['itemKey'],
        version=item['itemVersion'],
        publication=publication,
    )

    zotero_extractor_log.save()
