# -*- coding: utf-8 -*-

from django.conf import settings
from django.db.models import Max
from django.template.defaultfilters import slugify

from entities.events.models import Event
from entities.news.models import News, PublicationRelatedToNews
from entities.persons.models import Person, Nickname
from entities.projects.models import Project, RelatedPublication
from entities.publications.models import *
from entities.utils.models import Tag, City, Country
from extractors.zotero.models import ZoteroExtractorLog
from labman_setup.models import ZoteroConfiguration
from labman_ud.util import nslugify, get_or_default

from datetime import datetime
from dateutil import parser
from pyzotero import zotero
from pyzotero.zotero_errors import HTTPError

import logging
import os
import re
import socket
import time


logger = logging.getLogger(__name__)

JCR_PATTERN = r'(jcr|if)(-*)(\d(\.|\,)\d+)'
ACCEPTED_ATTACHMENT_FORMATS = ('.pdf', '.doc', '.docx')


###     get_zotero_variables()
####################################################################################################

def get_zotero_variables():

    zot = get_or_default(ZoteroConfiguration)

    if zot:
        return zot.api_key, zot.library_id, zot.library_type

    else:
        logger.warn(u"ZoteroConfiguration() object not configured in admin panel")

        return '', '', ''


###     get_zotero_connection()
####################################################################################################
def get_zotero_connection():
    api_key, library_id, library_type = get_zotero_variables()
    zot = zotero.Zotero(library_id=library_id, library_type=library_type, api_key=api_key)

    return zot


###     get_last_zotero_version()
####################################################################################################

def get_last_zotero_version():
    zot = get_zotero_connection()

    return int(zot.last_modified_version())


###     get_last_synchronized_zotero_version()
####################################################################################################

def get_last_synchronized_zotero_version():
    try:
        last_version = ZoteroExtractorLog.objects.all().aggregate(Max('version'))['version__max']

        if last_version is None:
            last_version = 0

    except:
        last_version = 0

    return int(last_version)


###     extract_publications_from_zotero(from_version)
####################################################################################################

def extract_publications_from_zotero(from_version):

    from_version = int(from_version)
    last_zotero_version = get_last_zotero_version()

    if from_version == last_zotero_version:
        logger.info(u"Labman is updated to the last version in Zotero (%d)" % last_zotero_version)

        return []

    else:
        if from_version > last_zotero_version:

            # This should never happen, but just in case, we solve the error by syncing the penultimate version in Zotero
            from_version = last_zotero_version - 1
            logger.warn(u"Asked 'from_version' was greater than 'last_zotero_version'. Strange...")

        # In case of a reset, save relationships between publications and news
        publications_related_to_news = []

        if from_version == 0:
            logger.info(u"A publication DB reset is ordered")

            for item_to_be_saved in PublicationRelatedToNews.objects.all():
                publications_related_to_news.append((
                    item_to_be_saved.news.title,
                    item_to_be_saved.publication.title
                ))

            Publication.objects.all().delete()
            # Just in case any legacy ZoteroExtractorLog() instances are left behind
            ZoteroExtractorLog.objects.all().delete()

        # Retrieve publications since required zotero version
        logger.info(u"Getting items since version %d" % from_version)
        logger.info(u"Last version in Zotero is %d" % last_zotero_version)

        zot = get_zotero_connection()

        total_items = []
        start = 0
        limit = 100

        items = zot.items(since=from_version, limit=limit, start=start)
        total_items.extend(items)

        while len(items) > 0:
            start += limit

            logger.debug(u"%s results found. Trying with ?start=%s" % (len(items), start))

            items = zot.items(since=from_version, limit=limit, start=start)

            if items:
                logger.debug(u"Last paper added: %s" % (items[-1]['data']['dateAdded']))

            total_items.extend(items)

        items = total_items

        logger.info(u"")
        logger.info(u"%d new items (includes attachments as items)" % len(items))

        items_ordered = {}
        attachments = []

        # Versioning control
        highest_detected_version = 0
        highest_parsed_version = 0

        for item in items:
            if item['version'] > highest_detected_version:
                highest_detected_version = item['version']

            if item['data']['itemType'] == 'attachment':
                if 'filename' in item['data']:
                    if item['data']['filename'].lower().endswith(ACCEPTED_ATTACHMENT_FORMATS):
                        attachments.append(item)

                    else:
                        logger.warn(u"\tInvalid attachment >> %s" % item['data']['filename'])

                else:
                    logger.warn(u"Could not identify attachment's filename")

            else:
                item_id = item['key']
                items_ordered[item_id] = item

        attachment_number = 0

        for a in attachments:
            if 'parentItem' in a['data']:
                attachment_number += 1
                parent_id = a['data']['parentItem']

                if parent_id in items_ordered.keys():
                    items_ordered[parent_id]['attachment'] = a

                else:
                    # Only the attachment has been modified
                    parent_publication = zot.item(parent_id)
                    publications = Publication.objects.filter(zotero_key=parent_publication['key'])

                    for publication in publications:
                        _save_attachment(a['key'], publication.slug, a['data']['filename'])
            else:
                logger.warn(u"%s" % a['data'].get('title', 'The user did not even added a title'))

        number_of_items = len(items_ordered)

        logger.info(u"")
        logger.info(u"%d items to be parsed (%d attachments)" % (number_of_items, attachment_number))

        for pos, i_id in enumerate(items_ordered):
            item = items_ordered[i_id]
            publication_type = item['data']['itemType']

            logger.info(u"  [%s/%s][%s][%s] > %s" % (
                pos + 1,
                number_of_items,
                datetime.strftime(datetime.now(), "%d/%b/%Y %H:%M:%S"),
                publication_type,
                item['data'].get('title', 'No title')
            ))

            generate_publication(item)

            if item['version'] > highest_parsed_version:
                highest_parsed_version = item['version']

        if highest_parsed_version == highest_detected_version:
            logger.info(u"Latest parsed item was a valid one")

        else:
            logger.info(u"Latest parsed item was not a valid one, versioning must be fixed")

            ZoteroExtractorLog.objects.create(
                item_key=u'VERSION_FIX',
                version=highest_detected_version,
            )

        # In case of a reset, reset saved relationships between publications and news
        if len(publications_related_to_news) > 0:
            logger.info(u"")
            logger.info(u"Restoring removed PublicationRelatedToNews() instances")

        for index, saved_link in enumerate(publications_related_to_news):
            news = get_or_default(News, title=saved_link[0])
            publication = get_or_default(Publication, title=saved_link[1])

            if news and publication:
                PublicationRelatedToNews.objects.create(
                    publication=publication,
                    news=news,
                )

                logger.info(u"[%d/%d] Link created" % (index + 1, len(publications_related_to_news)))

            else:
                logger.info(u"[%d/%d] Link NOT created: %s" % (index + 1, len(publications_related_to_news), str(saved_link)))


###     generate_publication(item)
####################################################################################################

def generate_publication(item):

    existing_publications = Publication.objects.filter(zotero_key=item['key']).all()

    for existing_publication in existing_publications:
        # There should 0 or 1 publication for that zotero key but just in case we run a "for"
        PublicationAuthor.objects.filter(publication=existing_publication).all().delete()
        PublicationEditor.objects.filter(publication=existing_publication).all().delete()
        PublicationTag.objects.filter(publication=existing_publication).all().delete()
        PublicationRank.objects.filter(publication=existing_publication).all().delete()
        RelatedPublication.objects.filter(publication=existing_publication).all().delete()
        existing_publication.delete()

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
        # this should not happen
        logger.warn(u"Publication type is ATTACHMENT")
        pass

    elif publication_type == 'thesis':
        parse_thesis(item)

    else:
        logger.warn(u"NOT parsed: %s" % publication_type)


###############################################################################
###############################################################################
# Item parsing
###############################################################################
###############################################################################


###     parse_journal_article(item)
####################################################################################################

def parse_journal_article(item):
    journal_article = JournalArticle()

    journal_article.zotero_key = item['key']

    journal_article.title = item['data']['title']
    journal_article.short_title = _extract_short_title(item)

    journal_article.abstract = _assign_if_exists(item, 'abstractNote')
    journal_article.pages = _assign_if_exists(item, 'pages')
    journal_article.doi = _extract_doi(item)

    journal_article.parent_journal = parse_journal(item)

    journal_article.published = _parse_date(item)
    journal_article.year = journal_article.published.year

    journal_article.bibtex = _extract_bibtex(item['key'])

    journal_article.save()

    _save_publication_authors(_extract_authors(item), journal_article)

    _extract_tags(item, journal_article)

    if 'attachment' in item:
        _save_attachment(item['attachment']['key'], journal_article.slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, journal_article)


###     parse_journal(item)
####################################################################################################

def parse_journal(item):
    journal_slug = nslugify(item['data']['publicationTitle'], _parse_date(item).year, item['data'].get('volume'), item['data'].get('issue'))

    journal = get_or_default(Journal, Journal(), slug=journal_slug)

    journal.title = item['data']['publicationTitle']

    journal.issn = _assign_if_exists(item, 'ISSN')
    journal.volume = _assign_if_exists(item, 'volume')
    journal.publisher = _assign_if_exists(item, 'publisher')
    journal.place = _assign_if_exists(item, 'place')
    journal.journal_abbreviation = _assign_if_exists(item, 'journalAbbrevation')
    journal.issue = _assign_if_exists(item, 'issue')

    journal.published = _parse_date(item)
    journal.year = journal.published.year

    journal.save()

    return journal


###     parse_conference_paper(item)
####################################################################################################

def parse_conference_paper(item):
    conference_paper = ConferencePaper()

    conference_paper.zotero_key = item['key']

    conference_paper.title = item['data']['title']
    conference_paper.short_title = _extract_short_title(item)

    conference_paper.abstract = _assign_if_exists(item, 'abstractNote')
    conference_paper.pages = _assign_if_exists(item, 'pages')
    conference_paper.doi = _extract_doi(item)

    conference_paper.parent_proceedings = parse_proceedings(item)
    conference_paper.presented_at = parse_conference(item, conference_paper.parent_proceedings)

    conference_paper.published = _parse_date(item)
    conference_paper.year = conference_paper.published.year

    conference_paper.bibtex = _extract_bibtex(item['key'])

    conference_paper.save()

    _save_publication_authors(_extract_authors(item), conference_paper)

    _extract_tags(item, conference_paper)

    if 'attachment' in item:
        _save_attachment(item['attachment']['key'], conference_paper.slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, conference_paper)


###     parse_proceedings(item)
####################################################################################################

def parse_proceedings(item):
    if item['data']['proceedingsTitle'] != '':
        proceedings_title = item['data']['proceedingsTitle']

    else:
        if item['data']['conferenceName'] != '':
            proceedings_title = 'Proceedings of conference: %s' % item['data']['conferenceName']

        else:
            proceedings_title = 'Proceedings for article: %s' % item['data']['title']

    proceedings = get_or_default(
        Proceedings,
        Proceedings(),
        slug=nslugify(proceedings_title, _parse_date(item).year, item['data'].get('volume')),
        year=_parse_date(item).year,
    )

    proceedings.title = proceedings_title

    proceedings.isbn = _assign_if_exists(item, 'ISBN')
    proceedings.volume = _assign_if_exists(item, 'volume')
    proceedings.series = _assign_if_exists(item, 'series')
    proceedings.publisher = _assign_if_exists(item, 'publisher')
    proceedings.place = _assign_if_exists(item, 'place')

    proceedings.published = _parse_date(item)
    proceedings.year = proceedings.published.year

    proceedings.save()

    return proceedings


###     parse_conference(item, proceedings)
####################################################################################################

def parse_conference(item, proceedings):
    if 'conferenceName' in item['data'] and item['data']['conferenceName'] != '':
        event = get_or_default(
            Event,
            Event(),
            slug=nslugify(item['data']['conferenceName'], _parse_date(item).year),
        )

        event.event_type = 'Academic event'

        event.full_name = item['data']['conferenceName']

        if 'place' in item['data'] and item['data']['place'] != '':
            places_list = item['data']['place'].split(', ')

            if len(places_list) == 2:
                city_name = places_list[0]
                country_name = places_list[1]

                event_location = ''

                if city_name and city_name != '':
                    city, created = City.objects.get_or_create(
                        slug=slugify(city_name),
                        defaults={
                            'full_name': city_name,
                        },
                    )

                else:
                    city = None

                if country_name and country_name != '' and city:
                    country, created = Country.objects.get_or_create(
                        slug=slugify(country_name),
                        defaults={
                            'full_name': country_name,
                        },
                    )

                    if city:
                        city.country = country
                        city.save()

                else:
                    country = None

                try:
                    event_location = '%s (%s)' % (city_name, country_name)
                except:
                    event_location = ''

                event.host_city = city
                event.host_country = country

                event.location = event_location

        event.start_date = _parse_date(item)
        event.year = event.start_date.year

        event.proceedings = proceedings

        event.save()

        return event

    else:
        return None


###     parse_book_section(item)
####################################################################################################

def parse_book_section(item):
    book_section = BookSection()

    book_section.zotero_key = item['key']

    book_section.title = item['data']['title']
    book_section.short_title = _extract_short_title(item)

    book_section.abstract = _assign_if_exists(item, 'abstractNote')
    book_section.pages = _assign_if_exists(item, 'pages')
    book_section.doi = _extract_doi(item)

    book_section.parent_book = parse_book(item)

    book_section.published = _parse_date(item)
    book_section.year = book_section.published.year

    book_section.bibtex = _extract_bibtex(item['key'])

    book_section.save()

    _save_publication_authors(_extract_authors(item), book_section)

    _extract_tags(item, book_section)

    if 'attachment' in item:
        _save_attachment(item['attachment']['key'], book_section.slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, book_section)


###     parse_book(item)
####################################################################################################

def parse_book(item):

    book = get_or_default(
        Book,
        Book(),
        slug=nslugify(item['data']['bookTitle'], _parse_date(item).year, item['data'].get('volume'), item['data'].get('series')),
        year=_parse_date(item).year,
    )

    book.title = item['data']['bookTitle']

    book.isbn = _assign_if_exists(item, 'ISBN')
    book.volume = _assign_if_exists(item, 'volume')
    book.series = _assign_if_exists(item, 'series')
    book.publisher = _assign_if_exists(item, 'publisher')
    book.place = _assign_if_exists(item, 'place')

    book.published = _parse_date(item)
    book.year = book.published.year

    book.save()

    _save_publication_editors(_extract_editors(item), book)

    return book


###     parse_authored_book(item)
####################################################################################################

def parse_authored_book(item):
    book = Book()

    book.zotero_key = item['key']

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

    book.published = _parse_date(item)
    book.year = book.published.year

    book.bibtex = _extract_bibtex(item['key'])

    book.save()

    _save_publication_authors(_extract_authors(item), book)

    _extract_tags(item, book)

    if 'attachment' in item:
        _save_attachment(item['attachment']['key'], book.slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, book)


###     parse_magazine_article(item)
####################################################################################################

def parse_magazine_article(item):
    magazine_article = MagazineArticle()

    magazine_article.zotero_key = item['key']

    magazine_article.title = item['data']['title']
    magazine_article.short_title = _extract_short_title(item)

    magazine_article.abstract = _assign_if_exists(item, 'abstractNote')
    magazine_article.pages = _assign_if_exists(item, 'pages')
    magazine_article.doi = _extract_doi(item)

    magazine_article.parent_magazine = parse_magazine(item)

    magazine_article.published = _parse_date(item)
    magazine_article.year = magazine_article.published.year

    magazine_article.bibtex = _extract_bibtex(item['key'])

    magazine_article.save()

    _save_publication_authors(_extract_authors(item), magazine_article)

    _extract_tags(item, magazine_article)

    if 'attachment' in item:
        _save_attachment(item['attachment']['key'], magazine_article.slug, item['attachment']['data']['filename'])

    _save_zotero_extractor_log(item, magazine_article)


###     parse_magazine(item)
####################################################################################################

def parse_magazine(item):

    magazine = get_or_default(
        Magazine,
        Magazine(),
        slug=nslugify(item['data']['publicationTitle'], _parse_date(item).year, item['data'].get('volume'), item['data'].get('issue')),
        year=_parse_date(item).year,
    )

    magazine.title = item['data']['publicationTitle']

    magazine.issn = _assign_if_exists(item, 'ISSN')
    magazine.volume = _assign_if_exists(item, 'volume')
    magazine.issue = _assign_if_exists(item, 'issue')

    magazine.published = _parse_date(item)
    magazine.year = magazine.published.year

    magazine.save()

    return magazine


###     parse_thesis(item)
####################################################################################################

def parse_thesis(item):
    author = _extract_authors(item)[0]

    thesis = get_or_default(
        Thesis,
        slug=slugify(item['data']['title']),
    )

    if not thesis:
        logger.warn(u"")
        logger.warn(u"%s should register his/her thesis using labman's admin page" % author)


###############################################################################
###############################################################################
# Common methods
###############################################################################
###############################################################################


###     _extract_short_title(item)
####################################################################################################

def _extract_short_title(item):
    if item['data'].get('shortTitle'):
        return item['data']['shortTitle']
    else:
        index = item['data']['title'].find(':')

        if index != -1:
            return item['data']['title'][:index]


###     _assign_if_exists(item, key)
####################################################################################################

def _assign_if_exists(item, key):
    if item['data'].get(key):
        return item['data'][key]


###     _extract_doi(item)
####################################################################################################

def _extract_doi(item):
    DOI_ORG_BASE_URL = 'http://dx.doi.org/'

    if 'DOI' in item['data']:
        if item['data']['DOI'] != '':
            return item['data']['DOI']

    elif 'url' in item['data']:
        if item['data']['url'] != '' and DOI_ORG_BASE_URL in item['data']['url']:
            base_url_end_index = len(DOI_ORG_BASE_URL)
            underscore_index = item['data']['url'].find('_') if item['data']['url'].find('_') != -1 else len(item['data']['url'])

            return item['data']['url'][base_url_end_index:underscore_index]


###     _parse_date(item)
####################################################################################################

def _parse_date(item):

    try:
        date_string = item['data']['date']
        parsed_date = parser.parse(date_string, fuzzy=True, default=datetime.today())

    except ValueError:
        try:
            date_chunks = date_string.split()
            parsed_date = parser.parse(date_chunks[0], fuzzy=True, default=datetime.today())

        except:
            try:
                alternate_date_string = item['meta']['parsedDate']
                parsed_date = parser.parse(alternate_date_string, fuzzy=True, default=datetime.today())

            except ValueError:
                try:
                    date_chunks = alternate_date_string.split()
                    parsed_date = parser.parse(date_chunks[0], fuzzy=True, default=datetime.today())

                except:
                    parsed_date = datetime.today()

    return parsed_date


###     _extract_bibtex(item_key)
####################################################################################################

def _extract_bibtex(item_key):
    zot = get_zotero_connection()

    counter = 4
    while counter >= 0:
        counter -= 1

        try:
            item = zot.item(item_key, format='bibtex')

        except (HTTPError, socket.error) as e:
            logger.debug(u"Error %s. Retrying in 5 seconds" % e)
            time.sleep(5)
            if counter == 0:
                raise
        else:
            break

    return item


###     _extract_authors(item)
####################################################################################################

def _extract_authors(item):
    authors = []

    if 'creators' in item['data'] and len(item['data']['creators']) > 0:
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

                author, created = Person.objects.get_or_create(
                    slug=author_slug,
                    defaults={
                        'first_name': author_first_name,
                        'first_surname': author_first_surname,
                    },
                )

                if not author:
                    try:
                        nick = Nickname.objects.filter(slug=author_slug).first()

                    except:
                        nick = None

                    if nick:
                        author, created = Person.objects.get_or_create(
                            id=nick.person.id,
                            defaults={
                                'first_name': author_first_name,
                                'first_surname': author_first_surname,
                            },
                        )

                authors.append(author)

    return authors


###     _save_publication_authors(authors, publication)
####################################################################################################

def _save_publication_authors(authors, publication):
    order = 1

    PublicationAuthor.objects.filter(publication=publication).all().delete()

    for author in authors:
        publication_author = PublicationAuthor(
            author=author,
            publication=publication,
            position=order,
        )

        publication_author.save()

        order += 1


###     _extract_tags(item, publication)
####################################################################################################

def _extract_tags(item, publication):

    # Clean ranking and projects so as to ensure that it's correctly synchronized
    PublicationRank.objects.filter(publication=publication).all().delete()
    RelatedPublication.objects.filter(publication=publication).all().delete()
    PublicationTag.objects.filter(publication=publication).all().delete()

    if 'tags' in item['data'] and len(item['data']['tags']) > 0:
        for tag_item in item['data']['tags']:
            tag_name = tag_item['tag'].encode('utf-8')

            if _determine_if_tag_is_special(tag_name, publication):
                pass

            else:
                tag, created = Tag.objects.get_or_create(
                    slug=slugify(tag_name),
                    defaults={
                        'name': tag_name,
                    },
                )

                publication_tag = PublicationTag(
                    tag=tag,
                    publication=publication,
                )

                publication_tag.save()


###     _save_zotero_extractor_log(item, publication)
####################################################################################################

def _save_zotero_extractor_log(item, publication):
    zotero_extractor_log = ZoteroExtractorLog(
        item_key=item['key'],
        version=item['version'],
        publication=publication,
    )

    zotero_extractor_log.save()


###     _save_attachment(attachment_id, publication_slug, filename)
####################################################################################################

def _save_attachment(attachment_id, publication_slug, filename):
    zot = get_zotero_connection()
    counter = 4

    while counter >= 0:
        counter -= 1

        try:
            item = zot.file(attachment_id)

        except (HTTPError, socket.error) as e:
            logger.debug(u"Error %s. Retrying in 5 seconds" % e)
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


###     _extract_editors(item)
####################################################################################################

def _extract_editors(item):
    editors = []

    if 'creators' in item['data'] and len(item['data']['creators']) > 0:
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

                editor = get_or_default(
                    Person,
                    slug=editor_slug,
                )

                if not editor:
                    nick = get_or_default(
                        Nickname,
                        slug=editor_slug,
                    )

                    if nick:
                        editor, created = Person.objects.get_or_create(
                            id=nick.person.id,
                            defaults={
                                'first_name': editor_first_name,
                                'first_surname': editor_first_surname,
                            },
                        )

                editors.append(editor)

    return editors


###     _save_publication_editors(editors, publication)
####################################################################################################

def _save_publication_editors(editors, publication):
    PublicationEditor.objects.filter(publication=publication).all().delete()

    for editor in editors:
        try:
            publication_editor = PublicationEditor(
                editor=editor,
                publication=publication,
            )

            publication_editor.save()

        except:
            logger.warn(u"The editor could not be saved. Please check.")


###     _determine_if_tag_is_special(tag, publication)
####################################################################################################

def _determine_if_tag_is_special(tag, publication):
    tag_slug = slugify(tag)
    jcr_match = re.match(JCR_PATTERN, tag.lower())

    project_slugs = Project.objects.all().values_list('slug', flat=True)
    ranking_slugs = Ranking.objects.all().values_list('slug', flat=True)

    special = True

    if tag_slug in ranking_slugs:
        ranking = Ranking.objects.get(slug=tag_slug)
        publication_ranking = PublicationRank(ranking=ranking, publication=publication)
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
