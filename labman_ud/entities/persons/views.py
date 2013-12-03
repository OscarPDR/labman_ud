# coding: utf-8

from django.core.urlresolvers import reverse
from django.db.models import Min, Max
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaultfilters import slugify

from charts.utils import nx_graph
from networkx.readwrite import json_graph

from .forms import PersonSearchForm
from .models import Person, Job, AccountProfile

from entities.organizations.models import Organization
from entities.projects.models import Project, AssignedPerson
from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag
from entities.utils.models import Role, Tag, Network

import json
import networkx as nx

# Create your views here.

REMOVABLE_TAGS = ['ISI', 'corea', 'coreb', 'corec', 'Q1', 'Q2']

OWN_ORGANIZATION_SLUGS = ['deustotech-internet', 'deustotech-telecom', 'morelab']


###########################################################################
# View: __get_person_data
###########################################################################

def __get_person_data(person):
    try:
        job = Job.objects.filter(person_id=person.id).order_by('-end_date')[0]
        organization = Organization.objects.get(id=job.organization_id)
        position = job.position

    except:
	job = None
        organization = None
        position = None

    return {
	'job': job,
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
        'company': data['organization'].short_name,
        'full_name': head.full_name,
        'gender': head.gender,
        'position': data['position'],
        'profile_picture_url': head.profile_picture,
        'slug': head.slug,
        'title': head.title,
        'profile_konami_code_picture': head.profile_konami_code_picture,
        'konami_code_position': head.konami_code_position,
    }


#########################
# View: person_index
#########################

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


#########################
# View: members
#########################

def members(request, organization_slug=None):
    member_konami_positions = []
    member_konami_profile_pictures = []
    members = []

    # MORElab only
    pr_internet = Person.objects.get(full_name='Diego López-de-Ipiña')
    head_of_internet = __get_head_data(pr_internet)

    pr_telecom = Person.objects.get(full_name='Jon Legarda')
    head_of_telecom = __get_head_data(pr_telecom)

    member_list = Person.objects.filter(is_active=True).exclude(id__in=[pr_internet.id, pr_telecom.id])
    member_list = member_list.order_by('first_surname', 'second_surname', 'first_name')
    # End of MORElab only

    for member in member_list:
        member_data = __get_person_data(member)

        if not organization_slug or (organization_slug == member_data['organization'].slug):
            members.append({
                'company': member_data['organization'].short_name,
                'full_name': member.full_name,
                'gender': member.gender,
                'position': member_data['position'],
                'profile_picture_url': member.profile_picture,
                'slug': member.slug,
                'title': member.title,
            })

            member_konami_positions.append(member.konami_code_position)
            member_konami_profile_pictures.append(member.profile_konami_code_picture)

    if organization_slug:
        organization = Organization.objects.get(slug=organization_slug)
    else:
        organization = None

    # dictionary to be returned in render_to_response()
    return_dict = {
        'head_of_internet': head_of_internet,
        'head_of_telecom': head_of_telecom,
        'member_konami_positions': member_konami_positions,
        'member_konami_profile_pictures': member_konami_profile_pictures,
        'members': members,
        'organization': organization,
        'organization_slug': organization_slug,
    }

    return render_to_response("members/index.html", return_dict, context_instance=RequestContext(request))


#########################
# View: former_members
#########################

def former_members(request, organization_slug=None):

    former_member_konami_positions = []
    former_member_konami_profile_pictures = []
    former_members = []

    organizations = Organization.objects.filter(slug__in=OWN_ORGANIZATION_SLUGS)

    former_member_ids = Job.objects.filter(organization__in=organizations).values('person_id')

    formber_member_list = Person.objects.filter(id__in=former_member_ids, is_active=False).order_by('slug')

    for former_member in formber_member_list:
        job = Job.objects.filter(person_id=former_member.id).order_by('-end_date')[0]
        organization = Organization.objects.get(id=job.organization_id)

        if not organization_slug or (organization_slug == organization.slug):
            former_members.append({
                'company': organization.short_name,
                'full_name': former_member.full_name,
                'gender': former_member.gender,
                'position': job.position,
                'profile_picture_url': former_member.profile_picture,
                'slug': former_member.slug,
                'title': former_member.title,
            })

            former_member_konami_positions.append(former_member.konami_code_position)
            former_member_konami_profile_pictures.append(former_member.profile_konami_code_picture)

    if organization_slug:
        organization = Organization.objects.get(slug=organization_slug)
    else:
        organization = None

    # dictionary to be returned in render_to_response()
    return_dict = {
        'former_member_konami_positions': former_member_konami_positions,
        'former_member_konami_profile_pictures': former_member_konami_profile_pictures,
        'former_members': former_members,
        'organization': organization,
        'organizations': organizations,
    }

    return render_to_response("former_members/index.html", return_dict, context_instance=RequestContext(request))


#########################
# View: member_info
#########################

def member_info(request, member_slug):

    member = Person.objects.get(slug=member_slug)

    try:
        job = Job.objects.get(person_id=member.id, end_date=None)
        position = job.position

    except:
        job = None
        position = None

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=member.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('-start_year', '-end_year')

        for project in project_objects:
            projects[role.name].append(project)

    publications = {}
    number_of_publications = {}

    min_year = Publication.objects.aggregate(Min('year'))
    max_year = Publication.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    years = []

    for year in range(min_year, max_year + 1):
        years.append(year)

    publication_types = PublicationType.objects.all()

    for publication_type in publication_types:
        pub_type = publication_type.name.encode('utf-8')
        publications[pub_type] = []
        number_of_publications[pub_type] = {}

        for year in years:
            number_of_publications[pub_type][year] = 0

    publication_ids = PublicationAuthor.objects.filter(author=member.id).values('publication_id')
    _publications = Publication.objects.filter(id__in=publication_ids).order_by('-year')

    has_publications = True if _publications else False

    for publication in _publications:
        pub_type = publication.publication_type.name.encode('utf-8')
        pub_year = publication.year
        publications[pub_type].append(publication)
        number_of_publications[pub_type][pub_year] = number_of_publications[pub_type][pub_year] + 1

    G = nx.Graph()

    pubs = Publication.objects.all()

    for pub in pubs:
        author_ids = PublicationAuthor.objects.filter(publication_id=pub.id).values('author_id')

        if author_ids:
            _list = [author_id['author_id'] for author_id in author_ids]

            for pos, author_id in enumerate(_list):
                for i in range(pos+1, len(_list)):
                    author = Person.objects.get(id=author_id)
                    author2 = Person.objects.get(id=_list[i])
                    G.add_edge(author.id, author2.id)

                    try:
                        G[author.id][author2.id]['weight'] += 1

                    except:
                        G[author.id][author2.id]['weight'] = 1
                    G.node[author.id]['name'] = author.full_name
                    G.node[author2.id]['name'] = author2.full_name

    try:
        G = nx_graph.analyze(G)
        ego_g = nx.ego_graph(G, member.id)
        data = json_graph.node_link_data(ego_g)

    except:
        data = {}

    # publication_tags_per_year = __clean_publication_tags(member.id, min_year, max_year)

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
        # 'publication_tags_per_year': publication_tags_per_year,
        'accounts': accounts,
        'data': json.dumps(data),
        'has_publications': has_publications,
        'member': member,
        'number_of_publications': number_of_publications,
        'position': position,
        'projects': projects,
        'publications': publications,
    }

    return render_to_response("members/info.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: former_member_info
###########################################################################

def former_member_info(request, former_member_slug):

    former_member = Person.objects.get(slug=former_member_slug)

    organizations = Organization.objects.filter(slug__in=OWN_ORGANIZATION_SLUGS)

    try:
        job = Job.objects.filter(person_id=former_member.id, organization_id__in=organizations).order_by('-end_date')[0]
        position = job.position

    except:
        job = None
        position = None

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=former_member.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('-start_year', '-end_year')

        for project in project_objects:
            projects[role.name].append(project)

    publications = {}
    number_of_publications = {}

    min_year = Publication.objects.aggregate(Min('year'))
    max_year = Publication.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    years = []

    for year in range(min_year, max_year + 1):
        years.append(year)

    publication_types = PublicationType.objects.all()

    for publication_type in publication_types:
        pub_type = publication_type.name.encode('utf-8')
        publications[pub_type] = []
        number_of_publications[pub_type] = {}

        for year in years:
            number_of_publications[pub_type][year] = 0

    publication_ids = PublicationAuthor.objects.filter(author=former_member.id).values('publication_id')
    _publications = Publication.objects.filter(id__in=publication_ids).order_by('-year')

    has_publications = True if _publications else False

    for publication in _publications:
        pub_type = publication.publication_type.name.encode('utf-8')
        pub_year = publication.year
        publications[pub_type].append(publication)
        number_of_publications[pub_type][pub_year] = number_of_publications[pub_type][pub_year] + 1

    G = nx.Graph()

    pubs = Publication.objects.all()

    for pub in pubs:
        author_ids = PublicationAuthor.objects.filter(publication_id=pub.id).values('author_id')

        if author_ids:
            _list = [author_id['author_id'] for author_id in author_ids]

            for pos, author_id in enumerate(_list):
                for i in range(pos+1, len(_list)):
                    author = Person.objects.get(id=author_id)
                    author2 = Person.objects.get(id=_list[i])
                    G.add_edge(author.id, author2.id)

                    try:
                        G[author.id][author2.id]['weight'] += 1

                    except:
                        G[author.id][author2.id]['weight'] = 1
                    G.node[author.id]['name'] = author.full_name
                    G.node[author2.id]['name'] = author2.full_name

    try:
        G = nx_graph.analyze(G)
        ego_g = nx.ego_graph(G, former_member.id)
        data = json_graph.node_link_data(ego_g)

    except:
        data = {}

    # publication_tags_per_year = __clean_publication_tags(former_member.id, min_year, max_year)

    # dictionary to be returned in render_to_response()
    return_dict = {
        # 'publication_tags_per_year': publication_tags_per_year,
        'data': json.dumps(data),
        'former_member': former_member,
        'has_publications': has_publications,
        'job': job,
        'number_of_publications': number_of_publications,
        'position': position,
        'projects': projects,
        'publications': publications,
    }

    return render_to_response("former_members/info.html", return_dict, context_instance=RequestContext(request))


#########################
# View: person_info
#########################

def person_info(request, slug):

    person = Person.objects.get(slug=slug)

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
        'person': person,
        'projects': projects,
        'publications': publications,
    }

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
