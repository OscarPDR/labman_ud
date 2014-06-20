# -*- encoding: utf-8 -*-

import threading
import weakref

from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.syndication.views import Feed

from collections import OrderedDict, defaultdict

from .forms import PersonSearchForm
from .models import Person, Job, AccountProfile

from entities.news.models import PersonRelatedToNews
from entities.events.models import Event
from entities.organizations.models import Organization, Unit
from entities.projects.models import Project, AssignedPerson
from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag
from entities.utils.models import Role, Tag, Network
from entities.publications.views import INDICATORS_TAG_SLUGS

# Create your views here.

REMOVABLE_TAGS = ['ISI', 'corea', 'coreb', 'corec', 'Q1', 'Q2']
UNIT_ORGANIZATION_IDS = Unit.objects.all().values_list('organization', flat=True)

# Status
MEMBER = 'member'
FORMER_MEMBER = 'former_member'


###########################################################################
# View: __get_person_data
###########################################################################

def __get_person_data(person):
    try:
        job = Job.objects.filter(person_id=person.id).order_by('-end_date')[0]
        organization = Organization.objects.get(id=job.organization_id)
        position = job.position

    except:
        organization = None
        position = None

    return {
        'person': person,
        'organization': organization,
        'position': position,
    }


###########################################################################
# View: __get_head_data
###########################################################################

def __get_head_data(head):
    data = __get_person_data(head)

    return {
        'organization': str(data['organization'].short_name),
        'organization_slug': str(data['organization'].slug),
        'full_name': str((head.full_name).encode('utf-8')),
        'gender': str(head.gender),
        'position': str(data['position']),
        'profile_picture_url': str(head.profile_picture.name),
        'slug': str(head.slug),
        'title': str(head.title),
        'profile_konami_code_picture': str(head.profile_konami_code_picture.name),
        'konami_code_position': str(head.konami_code_position),
    }


###########################################################################
# View: person_index
###########################################################################

def person_index(request, query_string=None):
    clean_index = True

    if query_string:
        query = slugify(query_string)
        persons = Person.objects.filter(slug__contains=query)
        clean_index = False
    else:
        persons = Person.objects.all()

    persons = persons.order_by('full_name')

    if request.method == 'POST':
        form = PersonSearchForm(request.POST)

        if form.is_valid():
            query_string = form.cleaned_data['text']
            clean_index = False

            return HttpResponseRedirect(reverse('view_person_query', kwargs={'query_string': query_string}))

    else:
        form = PersonSearchForm()

    persons_length = len(persons)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'persons': persons,
        'persons_length': persons_length,
        'query_string': query_string,
    }

    return render_to_response("persons/index.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: determine_person_info
###########################################################################

def determine_person_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    if person_status == MEMBER:
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if person_status == FORMER_MEMBER:
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))
    else:
        return HttpResponseRedirect(reverse('person_info', kwargs={'person_slug': person_slug}))


###########################################################################
# View: members
###########################################################################

def members(request, organization_slug=None):
    konami_positions = []
    konami_profile_pictures = []
    members = []

    organization = None
    units = Unit.objects.all()

    if organization_slug:
        organization = get_object_or_404(Organization, slug=organization_slug)
        filtered_units = Unit.objects.filter(organization=organization)
    else:
        filtered_units = units

    unit_head_person_ids = filtered_units.values_list('head', flat=True).order_by('order')
    unit_head_person_ids = [_id for _id in unit_head_person_ids if _id is not None]

    heads_of_unit = []

    for head_id in unit_head_person_ids:
        head = Person.objects.get(id=head_id)
        heads_of_unit.append(__get_head_data(head))
        konami_positions.append(head.konami_code_position)
        konami_profile_pictures.append(head.profile_konami_code_picture)

    member_list = Person.objects.filter(is_active=True).exclude(id__in=unit_head_person_ids)

    member_list = member_list.order_by('first_surname', 'second_surname', 'first_name')

    for member in member_list:
        member_data = __get_person_data(member)

        if not organization_slug or (organization_slug == member_data['organization'].slug):
            members.append({
                'organization': member_data['organization'].short_name,
                'organization_slug': member_data['organization'].slug,
                'full_name': member.full_name,
                'gender': member.gender,
                'position': member_data['position'],
                'profile_picture_url': member.profile_picture,
                'slug': member.slug,
                'title': member.title,
            })

            konami_positions.append(member.konami_code_position)
            konami_profile_pictures.append(member.profile_konami_code_picture)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': 'Members',
        'heads_of_unit': heads_of_unit,
        'konami_positions': konami_positions,
        'konami_profile_pictures': konami_profile_pictures,
        'members': members,
        'members_length': len(members) + len(heads_of_unit),
        'units': units,
        'organization': organization,
        'is_active_members': True,
    }

    return render_to_response("members/index.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: former_members
###########################################################################

def former_members(request, organization_slug=None):
    konami_positions = []
    konami_profile_pictures = []
    former_members = []

    organization = None
    units = Unit.objects.all()

    if organization_slug:
        organization = get_object_or_404(Organization, slug=organization_slug)
        filtered_units = Unit.objects.filter(organization=organization)
    else:
        filtered_units = units

    organization_ids = filtered_units.values_list('organization', flat=True)

    organizations = Organization.objects.filter(id__in=organization_ids)

    former_member_ids = Job.objects.filter(organization__in=organizations).values('person_id')

    former_member_list = Person.objects.filter(id__in=former_member_ids, is_active=False)
    former_member_list = former_member_list.order_by('first_surname', 'second_surname', 'first_name')

    former = {}
    ordered_dict = OrderedDict()

    for former_member in former_member_list:
        job = Job.objects.filter(person_id=former_member.id).order_by('-end_date')[0]

        if not job.end_date in former.keys():
            former[job.end_date] = []

        former[job.end_date].append(former_member)

    ordered_dict = OrderedDict(sorted(former.items(), key=lambda t: t[0], reverse=True))

    former_member_list = []

    for value in ordered_dict.values():
        for item in value:
            former_member_list.append(item)

    for former_member in former_member_list:
        former_member_data = __get_person_data(former_member)

        if not organization_slug or (organization_slug == former_member_data['organization'].slug):
            former_members.append({
                'organization': former_member_data['organization'].short_name,
                'organization_slug': former_member_data['organization'].slug,
                'full_name': former_member.full_name,
                'gender': former_member.gender,
                'position': former_member_data['position'],
                'profile_picture_url': former_member.profile_picture,
                'slug': former_member.slug,
                'title': former_member.title,
            })

            konami_positions.append(former_member.konami_code_position)
            konami_profile_pictures.append(former_member.profile_konami_code_picture)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': 'Former members',
        'konami_positions': konami_positions,
        'konami_profile_pictures': konami_profile_pictures,
        'members': former_members,
        'members_length': len(former_members),
        'units': units,
        'organization': organization,
        'is_active_members': False,
    }

    return render_to_response("members/index.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_info
###########################################################################

def member_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': member.full_name,
        'member': member,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/info.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_projects
###########################################################################

def member_projects(request, person_slug, role_slug=None):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_projects', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_projects', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    projects = {}

    has_projects = False

    if role_slug:
        roles = [get_object_or_404(Role, slug=role_slug)]
    else:
        roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=member.id, role=role.id).values('project_id')
        if project_ids:
            has_projects = True
        project_objects = Project.objects.filter(id__in=project_ids).order_by('-start_year', '-end_year')

        for project in project_objects:
            projects[role.name].append(project)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'%s - Projects' % member.full_name,
        'member': member,
        'has_projects': has_projects,
        'projects': projects,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/projects.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_publications
###########################################################################

def member_publications(request, person_slug, publication_type_slug=None):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_publications', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_publications', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    publications = OrderedDict()

    publication_ids = PublicationAuthor.objects.filter(author=member.id).values('publication_id')

    # Get those tags which are indicators (ISI, JCR...)
    tags = Tag.objects.filter(slug__in=INDICATORS_TAG_SLUGS).values('id', 'slug')
    tags_by_slug = {}
    for tag in tags:
        tags_by_slug[tag['slug']] = tag['id']

    publication_tag_ids = PublicationTag.objects.filter(publication_id__in=publication_ids, tag__slug__in=INDICATORS_TAG_SLUGS).values('tag_id', 'publication_id')
    indicators_per_publication = defaultdict(list)
    for publication_tag_id in publication_tag_ids:
        indicators_per_publication[publication_tag_id['publication_id']].append(publication_tag_id['tag_id'])

    has_publications = True if publication_ids else False

    # Manage ordering
    jcr_name = 'JCR article'
    isi_name = 'ISI article'

    SPECIAL_ORDER = [jcr_name, isi_name, 'journal-article', 'conference-paper', 'book-section', 'phd-thesis']   # The rest afterwards in random order

    tag_names = {
        'q1': jcr_name,
        'q2': jcr_name,
        'q3': jcr_name,
        'q4': jcr_name,

    }

    SEPARATE_ISI = False
    if SEPARATE_ISI:
        tag_names['isi'] = isi_name

    if publication_type_slug:
        publication_types = [get_object_or_404(PublicationType, slug=publication_type_slug)]
        publication_query = Publication.objects.filter(id__in=publication_ids, publication_type__in=publication_types).order_by('-year')
    else:
        publication_types = PublicationType.objects.all()

        for current_key in SPECIAL_ORDER:

            found = False

            for publication_type in publication_types:
                if publication_type.slug == current_key:
                    publications[publication_type.name.encode('utf-8')] = []
                    found = True
                    break

            # Some keys do not really exist (such as JCR). Put it in that order anyway

            if not found:
                publications[current_key] = []

        publication_query = Publication.objects.filter(id__in=publication_ids).order_by('-year')

    publication_types_by_id = {}
    for publication_type in publication_types:
        publication_types_by_id[publication_type.id] = publication_type

    #
    # Efficiently (3 queries) retrieve the names of the coauthors
    all_coauthors_publications = PublicationAuthor.objects.filter(publication__in=publication_ids).values('author_id', 'publication_id', 'position')
    author_ids_per_publication_id = defaultdict(list)   # {
    #     publication_id : [ (author_id1, position1), (author2, position2) ... ]
    # }

    distinct_coauthors = set()
    for current_key in all_coauthors_publications:
        distinct_coauthors.add(current_key['author_id'])
        author_ids_per_publication_id[current_key['publication_id']].append((current_key['author_id'], current_key['position']))
    all_coauthors = Person.objects.filter(id__in=distinct_coauthors).values('id', 'full_name')
    coauthor_by_id = {}
    for coauthor in all_coauthors:
        coauthor_by_id[coauthor['id']] = coauthor['full_name']

    coauthors_per_publication = {
        # publication_id : [ full_name1, full_name2, full_name3 ]
    }
    for publication_id, coauthor_list in author_ids_per_publication_id.iteritems():
        author_list = []
        for author_id, _ in sorted(coauthor_list, lambda (author_id1, position1), (author_id2, position2): cmp(position1, position2)):
            author_list.append(coauthor_by_id[author_id])
        coauthors_per_publication[publication_id] = author_list

    parent_publications = Publication.objects.filter(has_part__in=publication_query)
    parent_publications_by_id = {}
    for parent_publication in parent_publications:
        parent_publications_by_id[parent_publication.id] = parent_publication

    events = Event.objects.filter(proceedings__in=publication_query)
    events_by_id = {}
    for event in events:
        events_by_id[event.id] = event

    for publication in publication_query:
        for tag_slug in tag_names:
            if tags_by_slug.get(tag_slug, -1) in indicators_per_publication[publication.id]:
                pub_type = tag_names[tag_slug]
                break
        else:
            pub_type = publication_types_by_id[publication.publication_type_id].name.encode('utf-8')

        parent_publication = parent_publications_by_id.get(publication.part_of_id, None)

        if pub_type not in publications:
            publications[pub_type] = []

        event = events_by_id.get(publication.presented_at_id, None)

        publications[pub_type].append((publication, parent_publication, ', '.join(coauthors_per_publication[publication.id]), event))

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'%s - Publications' % member.full_name,
        'member': member,
        'publications': publications,
        'has_publications': has_publications,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/publications.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_publication_bibtex
###########################################################################

def member_publication_bibtex(request, person_slug):
    member = get_object_or_404(Person, slug=person_slug)
    global_bibtex = __get_global_bibtex(member)

    return_dict = {
        'web_title': u'%s - Publications bibtex' % member.full_name,
        'member': member,
        'bibtex':  global_bibtex,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/bibtex.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_publication_bibtex_download
###########################################################################

def member_publication_bibtex_download(request, person_slug):
    member = get_object_or_404(Person, slug=person_slug)
    global_bibtex = __get_global_bibtex(member)
    response = HttpResponse(global_bibtex, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename="%s.bib"' % member.slug
    return response


###########################################################################
# View: member_news
###########################################################################

def member_news(request, person_slug):
    member = get_object_or_404(Person, slug=person_slug)
    person_news = PersonRelatedToNews.objects.filter(person=member).select_related('news').order_by('-news__created')
    news = OrderedDict()

    for news_person in person_news:
        news_piece = news_person.news
        year_month = u'%s %s' % (news_piece.created.strftime('%B'), news_piece.created.year)
        if not year_month in news:
            news[year_month] = []
        news[year_month].append(news_piece)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'%s - News' % member.full_name,
        'member': member,
        'news': news,
    }
    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response('members/news.html', return_dict, context_instance=RequestContext(request))


###########################################################################
# Feed: member news feeds
###########################################################################

class LatestUserNewsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestUserNewsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    def get_object(self, request, person_slug):
        self.__request.request = weakref.proxy(request)
        return get_object_or_404(Person, slug=person_slug)

    def title(self, obj):
        return "%s news" % obj.full_name

    def link(self, obj):
        url = reverse('member_news', kwargs={'person_slug': obj.slug})
        return self.__request.request.build_absolute_uri(url)

    def description(self, obj):
        return "News about %s" % obj.full_name

    def items(self, obj):
        return PersonRelatedToNews.objects.filter(person=obj).select_related('news').order_by('-news__created')[:30]

    def item_title(self, item):
        return item.news.title

    def item_description(self, item):
        return item.news.content

    def item_link(self, item):
        url = reverse('view_news', args=[item.news.slug])
        return self.__request.request.build_absolute_uri(url)


###########################################################################
# Feed: member publications feed
###########################################################################

class LatestUserPublicationFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestUserPublicationFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    def get_object(self, request, person_slug):
        self.__request.request = weakref.proxy(request)
        return get_object_or_404(Person, slug=person_slug)

    def title(self, obj):
        return "%s publications" % obj.full_name

    def link(self, obj):
        url = reverse('member_publications', kwargs={'person_slug': obj.slug})
        return self.__request.request.build_absolute_uri(url)

    def description(self, obj):
        return "Publications where %s is coauthor" % obj.full_name

    def items(self, obj):
        return PublicationAuthor.objects.filter(author=obj).select_related('publication').order_by('-publication__log_created')[:30]

    def item_title(self, item):
        return item.publication.title

    def item_description(self, item):
        return "New publication: %s " % item.publication.title

    def item_link(self, item):
        url = reverse('publication_info', args=[item.publication.slug])
        return self.__request.request.build_absolute_uri(url)


###########################################################################
# View: member_profiles
###########################################################################

def member_profiles(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_profiles', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_profiles', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    accounts = []
    account_profiles = AccountProfile.objects.filter(person_id=member.id).order_by('network__name')

    for account_profile in account_profiles:
        network = Network.objects.get(id=account_profile.network_id)
        account_item = {
            'base_url': network.base_url,
            'icon_url': network.icon,
            'network_name': network.name,
            'profile_id': account_profile.profile_id,
        }
        accounts.append(account_item)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'member': member,
        'accounts': accounts,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/profiles.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: member_graphs
###########################################################################

def member_graphs(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_graphs', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_graphs', kwargs={'person_slug': person_slug}))

    member = get_object_or_404(Person, slug=person_slug)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'member': member,
    }

    data_dict = __get_job_data(member)
    return_dict.update(data_dict)

    return render_to_response("members/graphs.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: person_info
###########################################################################

def person_info(request, person_slug):
    person_status = __determine_person_status(person_slug)

    # Redirect to correct URL template if concordance doesn't exist
    if (person_status == MEMBER) and ('/' + MEMBER not in request.path):
        return HttpResponseRedirect(reverse('member_info', kwargs={'person_slug': person_slug}))
    if (person_status == FORMER_MEMBER) and ('/' + FORMER_MEMBER not in request.path):
        return HttpResponseRedirect(reverse('former_member_info', kwargs={'person_slug': person_slug}))

    person = get_object_or_404(Person, slug=person_slug)

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=person.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('slug')

        for project in project_objects:
            projects[role.name].append(project)

    publication_ids = PublicationAuthor.objects.filter(author=person.id).values('publication_id')
    _publications = Publication.objects.filter(id__in=publication_ids).order_by('-year')

    publications = {}

    for publication_type in PublicationType.objects.all():
        pub_type = publication_type.name.encode('utf-8')
        publications[pub_type] = []

    for publication in _publications:
        pub_type = publication.publication_type.name.encode('utf-8')
        publications[pub_type].append(publication)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': person.full_name,
        'person': person,
        'projects': projects,
        'publications': publications,
    }###########################################################################
# View: member_profiles
###########################################################################

    return render_to_response("persons/info.html", return_dict, context_instance=RequestContext(request))


####################################################################################################
# __clean_publication_tags
####################################################################################################

def __clean_publication_tags(member_id, min_year, max_year):
    publication_ids = PublicationAuthor.objects.filter(author_id=member_id).values('publication_id')

    pub_tag_ids = PublicationTag.objects.filter(publication_id__in=publication_ids).values('tag_id')
    all_pub_tags = PublicationTag.objects.filter(publication_id__in=publication_ids).values('tag_id__name', 'publication_id__year')
    pub_tags = Tag.objects.filter(id__in=pub_tag_ids).values_list('name', flat=True).distinct()

    tags = [x for x in pub_tags if x not in REMOVABLE_TAGS]

    publication_tags_per_year = {}

    for t in tags:
        tag = t.encode('utf-8')
        publication_tags_per_year[tag] = {}

        for year in range(min_year, max_year + 1):
            publication_tags_per_year[tag][year] = 0

    for pub_tag in all_pub_tags:
        try:
            tag_name = pub_tag.get('tag_id__name').encode('utf-8')
            year = pub_tag.get('publication_id__year')

            publication_tags_per_year[tag_name][year] = publication_tags_per_year[tag_name][year] + 1

        except:
            pass

    return publication_tags_per_year


####################################################################################################
# __determine_person_status
####################################################################################################

def __determine_person_status(person_slug):
    person = get_object_or_404(Person, slug=person_slug)

    if person.is_active:
        return MEMBER
    else:
        organizations = Organization.objects.filter(id__in=UNIT_ORGANIZATION_IDS)
        all_member_ids = Job.objects.filter(organization__in=organizations).values('person_id')
        former_member_list_ids = Person.objects.filter(id__in=all_member_ids, is_active=False).values_list('id', flat=True)

        if person.id in former_member_list_ids:
            return FORMER_MEMBER
        else:
            return None


####################################################################################################
# __get_global_bibtex
####################################################################################################

def __get_global_bibtex(member):
    publication_ids = PublicationAuthor.objects.filter(author=member.id).values('publication_id')
    publications_bibtex = Publication.objects.filter(id__in=publication_ids).values_list('bibtex', flat=True).order_by('-year')
    global_bibtex = '\n\n'.join(publications_bibtex)
    return global_bibtex


####################################################################################################
# __group_by_key
####################################################################################################

def __group_by_key(stmt, key='id'):
    """ Given a QuerySet, provide a dictionary grouped by a key. Typically:

    __group_by_key( Foo.objects.all() )

    returns a dictionary where the key is the 'id' field:

    { 1 : FooObject(id=1), 2 : FooObject(id=2) , ... }

    TODO: there is probably something similar in the Django API
    """
    results_by_key = {}
    for result in stmt:
        if isinstance(result, dict):
            results_by_key[result[key]] = result
        else:
            results_by_key[getattr(result, key)] = result
    return results_by_key


####################################################################################################
# __get_job_data
####################################################################################################

def __get_job_data(member):
    company = None
    first_job = None
    last_job = None
    position = None

    organizations = Organization.objects.filter(id__in=UNIT_ORGANIZATION_IDS)

    try:
        jobs = Job.objects.filter(person_id=member.id, organization_id__in=organizations).order_by('end_date')
        first_job = jobs[0]
        last_job = jobs.reverse()[0]
        organization = Organization.objects.get(id=last_job.organization_id)
        company = organization.short_name
        position = last_job.position
    except:
        pass

    pr_role = Role.objects.get(slug='principal-researcher')
    project_ids = AssignedPerson.objects.filter(person_id=member.id).exclude(role_id=pr_role.id).values('project_id')
    publication_ids = PublicationAuthor.objects.filter(author=member.id).values_list('publication_id', flat=True)

    accounts = []
    account_profiles = AccountProfile.objects.filter(person_id=member.id).order_by('network__name')

    for account_profile in account_profiles:
        network = Network.objects.get(id=account_profile.network_id)
        account_item = {
            'base_url': network.base_url,
            'icon_url': network.icon,
            'network_name': network.name,
            'profile_id': account_profile.profile_id,
        }
        accounts.append(account_item)

    publication_types_by_id = __group_by_key(PublicationType.objects.values('id', 'name', 'slug'))
    publications_by_id = __group_by_key(Publication.objects.filter(id__in=publication_ids))
    publication_types_by_name = defaultdict(int)

    for publication_id in publication_ids:
        publication_object = publications_by_id[publication_id]
        publication_type_id = publication_object.publication_type_id
        publication_type_name = publication_types_by_id[publication_type_id]['name'].encode('utf-8')
        publication_type_slug = publication_types_by_id[publication_type_id]['slug']
        publication_types_by_name[publication_type_name, publication_type_slug] += 1

    pubtype_info = []
    for (pubtype_name, pubtype_slug), number in publication_types_by_name.items():
        pubtype_info.append((pubtype_slug, pubtype_name, number))

    return {
        'first_job': first_job,
        'last_job': last_job,
        'company': company,
        'position': position,
        'number_of_projects': len(project_ids),
        'number_of_publications': len(publication_ids),
        'accounts': accounts,
        'pubtype_info': pubtype_info,
    }
