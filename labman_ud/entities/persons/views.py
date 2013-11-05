# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.db.models import Sum, Min, Max

from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import Person, Job, AccountProfile
from .forms import PersonSearchForm

from entities.projects.models import Project, AssignedPerson

from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag

from entities.utils.models import Role, Tag, Network

from entities.organizations.models import Organization

import networkx as nx
from networkx.readwrite import json_graph
import json

import community

from collections import Counter, OrderedDict
from itertools import islice


# Create your views here.

PAGINATION_NUMBER = settings.EMPLOYEES_PAGINATION


#########################
# View: person_index
#########################

def person_index(request):
    persons = Person.objects.all().order_by('full_name')

    if request.method == 'POST':
        form = PersonSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            emps = []

            for person in persons:
                if query in person.slug:
                    emps.append(person)

            persons = emps

    else:
        form = PersonSearchForm()

    paginator = Paginator(persons, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        persons = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        persons = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        persons = paginator.page(paginator.num_pages)

    return render_to_response("persons/index.html", {
            'persons': persons,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: members
#########################

def members(request):

    members = []
    member_konami_positions = []

    member_list = Person.objects.filter(is_active=True)

    for member in member_list:
        try:
            job = Job.objects.filter(person_id=member.id).order_by('-end_date')[0]
            organization = Organization.objects.get(id=job.organization_id)
            company = organization.short_name
            position = job.position
        except:
            company = None
            position = None

        members.append({
            "title": member.title,
            "full_name": member.full_name,
            "company": company,
            "position": position,
            "profile_picture_url": member.profile_picture,
            "slug": member.slug,
            "gender": member.gender,
        })

        member_konami_positions.append(member.konami_code_position)

    return render_to_response("members/index.html", {
            'members': members,
            "member_konami_positions": member_konami_positions,
        },
        context_instance=RequestContext(request))


#########################
# View: former_members
#########################

def former_members(request):

    former_members = []

    # Change to own organization/s
    org_slugs = ['deustotech-internet', 'deustotech-telecom', 'morelab']
    organization_ids = Organization.objects.filter(slug__in=org_slugs).values('id')

    former_member_ids = Job.objects.filter(organization_id__in=organization_ids).values('person_id')

    formber_member_list = Person.objects.filter(id__in=former_member_ids, is_active=False).order_by('slug')

    for former_member in formber_member_list:
        job = Job.objects.filter(person_id=former_member.id).order_by('-end_date')[0]
        organization = Organization.objects.get(id=job.organization_id)
        former_members.append({
            "title": former_member.title,
            "full_name": former_member.full_name,
            "company": organization.short_name,
            "position": job.position,
            "profile_picture_url": former_member.profile_picture,
            "slug": former_member.slug,
            "gender": former_member.gender,
        })

    return render_to_response("former_members/index.html", {
            'former_members': former_members,
        },
        context_instance=RequestContext(request))


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
                    G.add_edge(author.id,author2.id)
                    try:
                        G[author.id][author2.id]['weight'] += 1
                    except:
                        G[author.id][author2.id]['weight'] = 1
                    G.node[author.id]['name'] = author.full_name
                    G.node[author2.id]['name'] = author2.full_name

    try:
        G = analyze_graph(G)
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
            'profile_id': account_profile.profile_id,
            'network_name': network.name,
            'base_url': network.base_url,
            'icon_url': network.icon,
        }
        accounts.append(account_item)


    return render_to_response("members/info.html", {
            'member': member,
            'position': position,
            'projects': projects,
            'publications': publications,
            'has_publications': has_publications,
            'number_of_publications': number_of_publications,
            # 'publication_tags_per_year': publication_tags_per_year,
            'accounts': accounts,
            'data': json.dumps(data),
        },
        context_instance=RequestContext(request))


###########################################################################
# View: former_member_info
###########################################################################

def former_member_info(request, former_member_slug):

    former_member = Person.objects.get(slug=former_member_slug)

    organization = Organization.objects.get(slug='deustotech-internet')

    try:
        job = Job.objects.filter(person_id=former_member.id, organization=organization.id).order_by('-end_date')[0]
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
                    G.add_edge(author.id,author2.id)
                    try:
                        G[author.id][author2.id]['weight'] += 1
                    except:
                        G[author.id][author2.id]['weight'] = 1
                    G.node[author.id]['name'] = author.full_name
                    G.node[author2.id]['name'] = author2.full_name

    try:
        G = analyze_graph(G)
        ego_g = nx.ego_graph(G, former_member.id)
        data = json_graph.node_link_data(ego_g)
    except:
        data = {}

    # publication_tags_per_year = __clean_publication_tags(former_member.id, min_year, max_year)

    return render_to_response("former_members/info.html", {
            'former_member': former_member,
            'job': job,
            'position': position,
            'projects': projects,
            'publications': publications,
            'has_publications': has_publications,
            'number_of_publications': number_of_publications,
            # 'publication_tags_per_year': publication_tags_per_year,
            'data': json.dumps(data),
        },
        context_instance=RequestContext(request))


#########################
# View: person_info
#########################

def person_info(request, slug):

    person = get_object_or_404(Person, slug=slug)

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=person.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('slug')
        for project in project_objects:
            projects[role.name].append(project)

    return render_to_response("persons/info.html", {
            'person': person,
            'projects': projects,
        },
        context_instance=RequestContext(request))


####################################################################################################
# __clean_publication_tags
####################################################################################################

def __clean_publication_tags(member_id, min_year, max_year):
    project_tags = Project.objects.all().values('id')

    publication_ids = PublicationAuthor.objects.filter(author_id=member_id).values('publication_id')

    publications = Publication.objects.filter(id__in=publication_ids)

    pub_tag_ids = PublicationTag.objects.filter(publication_id__in=publication_ids).values('tag_id')
    all_pub_tags = PublicationTag.objects.filter(publication_id__in=publication_ids).values('tag_id__name', 'publication_id__year')
    pub_tags = Tag.objects.filter(id__in=pub_tag_ids).values_list('name', flat=True).distinct()

    removable_items = ['ISI', 'corea', 'coreb', 'corec', 'Q1', 'Q2']

    tags = [x for x in pub_tags if x not in removable_items]

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


###########################################################################
###########################################################################
### analyze_graph
###########################################################################
###########################################################################

def analyze_graph(G):    
    components = []    

    components = nx.connected_component_subgraphs(G)
    
    i = 0
    
    for cc in components:            
        #Set the connected component for each group
        for node in cc:
            G.node[node]['component'] = i
      
        #Calculate the in component betweeness, closeness and eigenvector centralities        
        cent_betweenness = nx.betweenness_centrality(cc)              
        cent_eigenvector = nx.eigenvector_centrality_numpy(cc)
        cent_closeness = nx.closeness_centrality(cc)
        
        for name in cc.nodes():
            G.node[name]['cc-betweenness'] = cent_betweenness[name]
            G.node[name]['cc-eigenvector'] = cent_eigenvector[name]
            G.node[name]['cc-closeness'] = cent_closeness[name]
        
        i +=1     
    
    # Calculate cliques
    cliques = list(nx.find_cliques(G))
    j = 0
    processed_members = []
    for clique in cliques:
        for member in clique:
            if not member in processed_members:
                G.node[member]['cliques'] = []
                processed_members.append(member)
            G.node[member]['cliques'].append(j)
        j +=1
    
    #calculate degree    
    degrees = G.degree()
    for name in degrees:
        G.node[name]['degree'] = degrees[name]
          
    betweenness = nx.betweenness_centrality(G)
    eigenvector = nx.eigenvector_centrality_numpy(G)
    closeness = nx.closeness_centrality(G)
    pagerank = nx.pagerank(G)
    k_cliques = nx.k_clique_communities(G, 3)
    
    for name in G.nodes():
        G.node[name]['betweenness'] = betweenness[name]
        G.node[name]['eigenvector'] = eigenvector[name]
        G.node[name]['closeness'] = closeness[name]
        G.node[name]['pagerank'] = pagerank[name]
    
    for pos, k_clique in enumerate(k_cliques):
        for member in k_clique:
            G.node[member]['k-clique'] = pos

    partitions = community.best_partition(G)

    for key in partitions.keys():
        G.node[key]['modularity'] = partitions[key]
        # G.nodes()[key]['modularity'] = partitions[key]
        # G.node[element]['modularity'] = key
        
    return G