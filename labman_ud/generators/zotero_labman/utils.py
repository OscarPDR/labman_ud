from django.template.defaultfilters import slugify

from django.conf import settings
from django.utils.timezone import utc

from generators.zotero_labman.models import ZoteroLog
from entities.events.models import Event, EventType
from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag
from entities.organizations.models import Organization, OrganizationType
from entities.utils.models import Language, Tag
from entities.persons.models import Person, Nickname, Job
from entities.projects.models import Project, RelatedPublication, ProjectTag
from entities.news.models import PublicationRelatedToNews, NewsTag

from pyzotero import zotero
from dateutil import parser
from datetime import datetime

from sets import Set

import requests
import os
import re
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add the log message handler to the logger
#handler = logging.handlers.RotatingFileHandler(
#    getattr(settings, 'ZOTERO_LOG_PATH', 'zotero_labman.log'),
#    maxBytes=20000,
#    backupCount=5
#)
#logger.addHandler(handler)

# Dict with supported Zotero itemTypes, translated to LabMan's PublicationTypes
SUPPORTED_ITEM_TYPES = {
    'bookSection': 'Book section',
    'book': 'Book',
    'journalArticle': 'Journal article',
    'magazineArticle': 'Magazine article',
    'newspaperArticle': 'Newspaper article',
    'thesis': 'PhD thesis',
    'report': 'Technical Report',
    'patent': 'Misc',
    'presentation': 'Misc',
    'document': 'Misc',
    'conferencePaper': 'Conference paper',
}


def get_zotero_variables():
    # TODO: Check variables
    api_key = getattr(settings, 'ZOTERO_API_KEY', None)
    library_id = getattr(settings, 'ZOTERO_LIBRARY_ID', None)
    library_type = getattr(settings, 'ZOTERO_LIBRARY_TYPE', None)
    api_limit = 10

    return api_key, library_id, library_type, api_limit


def get_last_zotero_version():
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    r = requests.get('https://api.zotero.org/'+  library_type + 's/' + library_id + '/items?format=versions&limit=1&order=dateModified&key=' + api_key)
    # max_items = max(r.json().items(), key=operator.itemgetter(1))[1]
    max_items = r.json().items()[0][1]

    r = requests.get('https://api.zotero.org/'+  library_type + 's/' + library_id + '/items/trash?format=versions&limit=1&order=dateModified&key=' + api_key)
    max_trash = r.json().items()[0][1]

    return max(max_items, max_trash)


def parse_last_items(last_version, version=0, prefix='[NEW_ITEMS_SYNC]'):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)

    # Get the slugs of all the projects in labman to create pub-proj relationships (based on tag comparision)
    project_slugs = [slug['slug'] for slug in Project.objects.all().order_by('slug').values('slug')]

    # Dataset of backed up info from deleted publications
    backup_dataset = []

    if version == last_version:
        logger.info('Labman is already updated to last version in Zotero (%i)! :-)' % (last_version))
    else:
        if version > last_version:
            # This should not happend anytime, but in this case, we solve the error by syncing the penultimate version in Zotero
            logger.info('Labman version number (%i) is higher than Zotero\'s one (%i)... :-/ Solving the error...' % (version, last_version))
            version = last_version - 1

        logger.info('Getting items since version %i' % (version))
        logger.info('Last version in Zotero is %i' % (last_version))

        gen = zot.makeiter(zot.items(limit=api_limit, order='dateModified', sort='desc', newer=version))

        lastitems = []

        moreitems = True
        while moreitems:
            try:
                items = gen.next()
            except StopIteration:
                moreitems = False

            if items and items != lastitems:
                for item in items:
                    if item['itemType'] in SUPPORTED_ITEM_TYPES:
                        # Delete publication if exists
                        pub = None
                        try:
                            pub = ZoteroLog.objects.filter(zotero_key=item['key']).order_by('-created')[0].publication
                        except:
                            try:
                                pub = Publication.objects.get(slug=slugify(str(item['title'].encode('utf-8'))))
                            except:
                                pass

                        if pub:
                            logger.info('Item already exists! Deleting...')
                            backup_data = None
                            backup_data = delete_publication(pub)
                            if backup_data:
                                backup_dataset.extend(backup_data)

                        # Create new publication
                        logger.info('Creating new publication: %s' % (item['title']))
                        pub = None
                        pub, authors, tags, observations = get_publication_details(item)
                        if observations:
                            logger.info('Saved but... %s' % (observations))

                        logger.info('Saving publication...')

                        # Save publication
                        pub.save()

                        # Saving authors and tags (many-to-many fields)
                        logger.info('Saving authors and tags...')

                        order = 1
                        for author in authors:
                            pubauth = PublicationAuthor(
                                author=author,
                                publication=pub,
                                position=order
                            )
                            pubauth.save()
                            order += 1
                        for tag in tags:
                            pubtag = PublicationTag(
                                publication=pub,
                                tag=tag
                            )
                            pubtag.save()

                            tag_slug = slugify(str(tag.name.encode('utf-8')))

                            # Find publication - project relations through tags
                            if tag_slug in project_slugs:
                                logger.info('Saving found publication-project relationship: %s' % (tag.name))
                                try:
                                    pubproj = RelatedPublication(publication=pub, project=Project.objects.get(slug=tag_slug))
                                    pubproj.save()
                                except:
                                    logger.info('Unable to create the relationship :-/')

                        # Save log
                        zotlog = ZoteroLog(zotero_key=item['key'], updated=parser.parse(item['updated']), version=last_version, observations=observations)
                        zotlog.publication = pub
                        zotlog.save()
                        logger.info('OK!')

                        logger.info('-'*30)
                lastitems = items
        # Generate a log specifying that the sync has finished for X version (due to avoid synchronization errors)
        zotlog = ZoteroLog(zotero_key='-SYNCFINISHED-', updated=datetime.utcnow().replace(tzinfo=utc), version=last_version, observations='')
        zotlog.save()

        # Restore news of deleted items, if any
        logger.info('Restoring news of deleted items, if any')
        restore_news(backup_dataset)


def sync_deleted_items(last_version, version, prefix='[DELETE_SYNC]'):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)

    if version == last_version:
        logger.info('Labman is already updated to last version in Zotero (%i)! :-)' % (last_version))
    else:
        if version > last_version:
            # This should not happend anytime, but in this case, we solve the error by syncing the penultimate version in Zotero
            logger.info('Labman version number (%i) is higher than Zotero\'s one (%i)... :-/ Solving the error...' % (version, last_version))
            version = last_version - 1

        logger.info('Getting removed items since version %i' % (version))
        logger.info('Last version in Zotero is %i' % (last_version))
        logger.info('\n')

        gen = zot.makeiter(zot.trash(limit=api_limit, order='dateModified', sort='desc', newer=version))

        lastitems = []

        moreitems = True
        while moreitems:
            try:
                items = gen.next()
            except StopIteration:
                moreitems = False

            if items and items != lastitems:
                for item in items:
                    if item['itemType'] in SUPPORTED_ITEM_TYPES:
                        try:
                            pub = ZoteroLog.objects.filter(zotero_key=item['key']).order_by('-created')[0].publication
                            logger.info('Deleting %s...' % (item['title']))

                            delete_publication(pub)

                            zotlog = ZoteroLog(zotero_key=item['key'], updated=parser.parse(item['updated']), version=last_version, delete=True, publication=None)
                            zotlog.save()
                            logger.info('-'*30)
                        except:
                            pass
                lastitems = items
        # Generate a log specifying that the sync has finished for X version (due to avoid synchronization errors)
        zotlog = ZoteroLog(zotero_key='-SYNCFINISHED-', updated=datetime.utcnow().replace(tzinfo=utc), version=last_version, delete=True, observations='')
        zotlog.save()


def get_publication_details(item):
    pub = Publication()

    observations = ''

    # Publicaton type
    pub.publication_type, created = PublicationType.objects.get_or_create(name=SUPPORTED_ITEM_TYPES[item['itemType']])

    # Publication language
    if 'language' in item and item['language']:
        pub.language, created = Language.objects.get_or_create(
            slug=slugify(str(item['language'].encode('utf-8'))),
            defaults={'name': item['language']}
        )
    else:
        pub.language = None

    # Publication date / year
    try:
        pub.published = parser.parse(item['date'])
        pub.year = pub.published.year
    except:
        year = re.findall(r'\d{4}', item['date'])
        if year:
            pub.published = datetime(int(year[0]),1,1)
            pub.year = year[0]
        else:
            pub.published = None
            pub.year = '2030'
            error_msg = 'Error getting year from %s.' % (str(item['date']))
            logger.error(error_msg)
            observations = error_msg

    # University
    if 'university' in item and item['university']:
        organization_type, created = OrganizationType.objects.get_or_create(name='University')
        pub.university, created = Organization.objects.get_or_create(
            slug=slugify(str(item['university'].encode('utf-8'))),
            defaults={'organization_type': organization_type, 'full_name': item['university']}
        )

    # Common attributes for all publications
    pub.title = item['title']
    pub.abstract = item['abstractNote']
    pub.short_title = item['shortTitle'] if 'shortTitle' in item and item['shortTitle'] else None
    pub.doi = item['DOI'] if 'DOI' in item and item['DOI'] else None
    pub.pages = item['pages'] if 'pages' in item and item['pages'] else None
    pub.issue = item['issue'] if 'issue' in item and item['issue'] else None
    pub.book_title = item['bookTitle'] if 'bookTitle' in item and item['bookTitle'] else None

    # Attributes that can be both from publications and "parent" publications
    pub_subpub_attributes = {
        'journal_abbreviation': item['journalAbbrevation'] if 'journalAbbrevation' in item and item['journalAbbrevation'] else None,
        'series': item['series'] if 'series' in item and item['series'] else None,
        'series_number': item['seriesNumber'] if 'seriesNumber' in item and item['seriesNumber'] else None,
        'volume': item['volume'] if 'volume' in item and item['volume'] else None,
        'publisher': item['publisher'] if 'publisher' in item and item['publisher'] else None,
        'edition': item['edition'] if 'edition' in item and item['edition'] else None,
        'series_text': item['seriesText'] if 'seriesText' in item and item['seriesText'] else None,
        'isbn': item['ISBN'] if 'ISBN' in item and item['ISBN'] else None,
        'issn': item['ISSN'] if 'ISSN' in item and item['ISSN'] else None,
        'year': pub.year,
    }

    # If conference paper, create Conference event and Proceeding parent publication
    if item['itemType'] == 'conferencePaper':
        if item['conferenceName']:
            conf_name = item['conferenceName']
        else:
            conf_name = item['proceedingsTitle']
            conf_name = conf_name.replace('proc. of the ', '')
            conf_name = conf_name.replace('Proc. of the ', '')
            conf_name = conf_name.replace('proceedings of the ', '')
            conf_name = conf_name.replace('Proceedings of the ', '')

        proceedings_title = item['proceedingsTitle'] if item['proceedingsTitle'] else 'Proceedings of ' + conf_name

        pub_type_proceedings, created = PublicationType.objects.get_or_create(name='Proceedings')

        pub_subpub_attributes['abstract'] = proceedings_title
        pub_subpub_attributes['title'] = proceedings_title
        pub_subpub_attributes['publication_type'] = pub_type_proceedings

        proceedings, created = Publication.objects.get_or_create(
            slug = slugify(str(proceedings_title.encode('utf-8'))),
            defaults=pub_subpub_attributes
        )

        if proceedings.publication_type != pub_type_proceedings:
            proceedings.publication_type = pub_type_proceedings
            proceedings.save()

        event_type_academic, created = EventType.objects.get_or_create(name='Academic event')
        pub.presented_at, created = Event.objects.get_or_create(
            slug=slugify(str(conf_name.encode('utf-8'))),
            defaults={
                'full_name': conf_name,
                'event_type': event_type_academic,
                'year': pub.published.year,
                'location': item['place'],
                'proceedings': proceedings
            }
        )

        # Relation between the publication and its parent
        pub.part_of = proceedings

    # If journal, magazine or newspaper article or book section, create parent publication
    elif item['itemType'] in ['bookSection', 'journalArticle', 'magazineArticle', 'newspaperArticle']:
        if item['itemType'] == 'bookSection':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Book')
            parentpub_title = item['bookTitle'] if 'bookTitle' in item and item['bookTitle'] else 'Book ?'
        elif item['itemType'] == 'journalArticle':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Journal')
            parentpub_title = item['publicationTitle'] if 'publicationTitle' in item and item['publicationTitle'] else None
            if not parentpub_title:
                parentpub_title = item['journal_abbreviation'] if 'journalAbbrevation' in item and item['journalAbbrevation'] else 'Journal ?'
        elif item['itemType'] == 'magazineArticle':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Magazine')
            parentpub_title = item['publicationTitle'] if 'publicationTitle' in item and item['publicationTitle'] else 'Magazine ?'
        elif item['itemType'] == 'newspaperArticle':
            parentpub_type, created = PublicationType.objects.get_or_create(name='Newspaper')
            parentpub_title = item['publicationTitle'] if 'publicationTitle' in item and item['publicationTitle'] else 'Newspaper ?'

        pub_subpub_attributes['abstract'] = ' '
        pub_subpub_attributes['title'] = parentpub_title
        pub_subpub_attributes['publication_type'] = parentpub_type

        parentpub, created = Publication.objects.get_or_create(
            slug = slugify(str(parentpub_title.encode('utf-8'))),
            defaults=pub_subpub_attributes
        )

        if parentpub.publication_type != parentpub_type:
            parentpub.publication_type = parentpub_type
            parentpub.save()

        # Relation between the publication and its parent
        pub.part_of = parentpub

    # If it has no parent publication, all those attributes go to publication itself
    else:
        pub.__dict__.update(pub_subpub_attributes)

    # Get PDF attachments

    # Determine pdf path...
    # ...if the publication is presented at any event (conference, workshop, etc.), it will be stored like:
    #   publications/2012/ucami/title-of-the-paper.pdf
    # ...otherwise, it will be stored like:
    #   publications/2012/book-chapter/title-of-the-paper.pdf
    if pub.presented_at:
        sub_folder = pub.presented_at.slug
    else:
        sub_folder = pub.publication_type.slug
    pdf_path = '%s/%s/%s/%s' % ('publications', pub.year, sub_folder, slugify(str(pub.title.encode('utf-8'))) + '.pdf')

    has_attachment = get_attached_pdf(item['key'], pdf_path)
    if has_attachment:
        pub.pdf = pdf_path

    # Get bibtex
    pub.bibtex = get_bibtex(item['key'])

    # Authors
    # We save them later (when we save pub in DB) (many-to-many fields)
    authors = []
    for creator in item['creators']:
        if creator['creatorType'] == 'author':
            author_name = ''
            if 'name' in creator and creator['name']:
                author_name = str(creator['name'].encode('utf-8'))
                first_surname = author_name.split(' ')[-1]
                first_name = author_name.replace(' ' + first_surname, '')

            first_name = str(creator['firstName'].encode('utf-8')) if 'firstName' in creator and creator['firstName'] else 'John'
            first_surname = str(creator['lastName'].encode('utf-8')) if 'lastName' in creator and creator['lastName'] else 'Doe'

            if not author_name:
                author_name = '%s %s' % (first_name, first_surname)

            author_slug = slugify(author_name)
            try:
                # Check if author is in DB (comparing by slug)
                a = Person.objects.get(slug=author_slug)
            except:
                # If it isn't
                try:
                    # Check if author name correspond with any of the posible nicknames of the authors in DB
                    nick = Nickname.objects.get(slug=slugify(author_name))
                    a = nick.person
                except:
                    # If there is no reference to that person in the DB, create a new one
                    a = Person(
                       first_name=first_name,
                       first_surname=first_surname
                       )
                    a.save()
                    # TODO: Send email to admins notifying the creation of new person
            authors.append(a)

    # Tags
    tags = []

    for tag in item['tags']:
        tag_str = str(tag['tag'].encode('utf-8'))

        # Check if the publication has the 'jcrX.XXX' tag including the impact factor of the publication
        jcr_pattern = r'(jcr|if)(\d(\.|\,)\d+)'
        jcr_match = re.match(jcr_pattern, tag_str)
        if jcr_match:
            impact_factor = jcr_match.groups()[1]
            if jcr_match.groups()[2] == ',':
                impact_factor = impact_factor.replace(',', '.')
            if parentpub:
                parentpub.impact_factor = float(impact_factor)
                parentpub.save()
            else:
                pub.impact_factor = float(impact_factor)
        else:
            # If it doesn't, create the tag as normal
            if len(tag['tag']) <= 75:
                t, created = Tag.objects.get_or_create(
                    slug=slugify(tag_str),
                    defaults={'name': tag['tag']}
                )
                tags.append(t)

    return pub, authors, tags, observations


def get_attached_pdf(item_key, path):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)
    children = zot.children(item_key)

    for child in children:
        # Finde if there is any attached PDF
        if child['itemType'] == 'attachment' and child['contentType'] == 'application/pdf':
            logger.info('Getting attachment: ' + child['filename'] + '...')

            r = requests.get('https://api.zotero.org/'+  library_type + 's/'+ library_id + '/items/'+ child['key'] + '/file?key=' + api_key)

            # If the directory doesn't exist, create it
            pdf_dir = getattr(settings, 'MEDIA_ROOT', None) + '/' + os.path.dirname(path)
            if not os.path.exists(pdf_dir):
                os.makedirs(pdf_dir)

            with open(getattr(settings, 'MEDIA_ROOT', None) + '/' + path, 'wb') as pdffile:
                pdffile.write(r.content)

            return True

    return False


def get_bibtex(item_key):
    api_key, library_id, library_type, api_limit = get_zotero_variables()

    zot = zotero.Zotero(library_id, library_type, api_key)
    bibtex = zot.item(item_key, content='bibtex')
    return ''.join(bibtex)


def delete_publication(pub):
    # We return a list of backup dicts, of the publication and its children
    ret_list = []

    try:
        zot_key = ZoteroLog.objects.filter(publication=pub).order_by('-created')[0].zotero_key
    except IndexError:
        zot_key = None

    publ_proj = Set()
    if pub.projects.all():
        for proj in pub.projects.all():
            publ_proj.add(proj)

    # I don't understand why publ_news = pub.news.all() doesn't work as expected: the ret_dict is
    # generated correctly -with a list of news-, but when returned the list appears empty :-?
    publ_news = Set()
    if pub.news.all():
        for nw in pub.news.all():
            publ_news.add(nw)

    # Create restored data dictionary
    ret_dict = {
        'zot_key': zot_key,
        'publ_event': pub.presented_at,
        'publ_lang': pub.language,
        'publ_observations': pub.observations,
        'publ_uni': pub.university,
        'publ_parentpub': pub.part_of,
        'publ_proj': publ_proj,
        'publ_news': publ_news,
    } if zot_key else None

    if ret_dict:
        ret_list.append(ret_dict)

    # Delete PDF file
    if pub.pdf:
        try:
            os.remove(getattr(settings, 'MEDIA_ROOT', None) + '/' + str(pub.pdf))
        except:
            pass

    # Check and backup if it has any children before deleting it (otherwise they will be deleted without backing up)
    for part in pub.has_part.all():
        backup_data = None
        backup_data = delete_publication(part)
        if backup_data:
            ret_list.extend(backup_data)

    # Delete publication object
    pub.delete()

    return ret_list


def correct_nicks():
    for nick in Nickname.objects.all():
        try:
            bad_person = Person.objects.get(slug=nick.slug)

            if bad_person and bad_person != nick.person:
                logger.info('Deleting... %s' % bad_person.full_name)
                for pubauth in PublicationAuthor.objects.filter(author=bad_person):
                    logger.info('Changing authorship of %s' % pubauth.publication)
                    pubauth.author = nick.person
                    pubauth.save()
                bad_person.delete()
        except:
            pass


def restore_news(backup_dataset):
    for pub_backup in backup_dataset:
        pub = None
        try:
            pub = ZoteroLog.objects.filter(zotero_key=pub_backup['zot_key']).order_by('-created')[0].publication
        except:
            pass

        if pub:
            for nw in pub_backup['publ_news']:
                logger.info('Restoring %s - %s...' % (pub, nw))
                pn = PublicationRelatedToNews()
                pn.publication = pub
                pn.news = nw
                pn.save()

    logger.info('OK!')
    logger.info('-'*30)


###########################################################################
# def: remove_unrelated_persons()
###########################################################################

def remove_unrelated_persons():
    unused_person_ids = Set()
    organization_slugs = ['morelab', 'deustotech-internet', 'deustotech-telecom']

    all_persons = Person.objects.all()
    own_organizations = Organization.objects.filter(slug__in=organization_slugs)

    for person in all_persons:
        publications = person.publications.all()
        projects = person.projects.all()
        if (len(publications) == 0) and (len(projects) == 0):
            unused_person_ids.add(person.id)

    unused_persons = Person.objects.filter(id__in=unused_person_ids, is_active=False)

    persons_to_remove = Set()

    removed_objects = 0

    for person in unused_persons:
        jobs = Job.objects.filter(person=person, organization__in=own_organizations)
        if len(jobs) == 0:
            removed_objects += 1
            persons_to_remove.add(person)
            logger.info(' Person to be deleted: %s' % person.full_name)
            person.delete()

    logger.info('Removed %d items' % removed_objects)


###########################################################################
# def: remove_unrelated_tags()
###########################################################################

def remove_unrelated_tags():
    used_tag_ids = Set()

    for item in PublicationTag.objects.all():
        used_tag_ids.add(item.tag.id)

    for item in ProjectTag.objects.all():
        used_tag_ids.add(item.tag.id)

    for item in NewsTag.objects.all():
        used_tag_ids.add(item.tag.id)

    unused_tags = Tag.objects.exclude(id__in=used_tag_ids)

    removed_objects = 0

    for tag in unused_tags:
        logger.info(' Tag to be deleted: %s' % tag.name)
        tag.delete()
        removed_objects += 1

    logger.info('Removed %d items' % removed_objects)
