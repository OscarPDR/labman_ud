# coding: utf-8

from datetime import date

from django.db.models import Sum, Min, Max
from django.shortcuts import render_to_response
from django.template import RequestContext

from charts.utils import nx_graph
from networkx.readwrite import json_graph

from entities.funding_programs.models import FundingProgram
from entities.persons.models import Person
from entities.projects.models import Project, FundingAmount, Funding, AssignedPerson
from entities.publications.models import Publication, PublicationType, PublicationAuthor
from entities.utils.models import GeographicalScope, Role

import json
import networkx as nx


# Create your views here.


###########################################################################
# View: chart_index
###########################################################################

def chart_index(request):
    return render_to_response('charts/index.html')


###########################################################################
# View: funding_total_incomes
###########################################################################

def funding_total_incomes(request):
    path = str(request.path).replace('total_', '')

    min_year = FundingAmount.objects.aggregate(Min('year'))
    max_year = FundingAmount.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    incomes = []

    current_year = date.today().year

    for year in range(min_year, max_year + 1):
        income = FundingAmount.objects.filter(year=year).aggregate(value=Sum('own_amount'))
        if income['value'] is None:
            income['value'] = 0
        certainty = False if (year > current_year) else True
        incomes.append({'key': year, 'value': int(income['value']), 'certainty': certainty})

    # dictionary to be returned in render_to_response()
    return_dict = {
        'incomes': incomes,
        'path': path,
    }

    return render_to_response("charts/funding/total_incomes.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: funding_incomes_by_year
###########################################################################

def funding_incomes_by_year(request, year):
    path = str(request.path).replace('total_', '') + '/'

    incomes = {}

    geographical_scopes = GeographicalScope.objects.all()

    for geographical_scope in geographical_scopes:
        incomes[geographical_scope.name] = 0

    year_incomes = FundingAmount.objects.filter(year=year)

    for year_income in year_incomes:
        funding = Funding.objects.get(id=year_income.funding_id)
        funding_program = FundingProgram.objects.get(id=funding.funding_program.id)
        scope = funding_program.geographical_scope.name
        incomes[scope] = incomes[scope] + int(year_income.own_amount)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'incomes': incomes,
        'path': path,
        'year': year,
    }

    return render_to_response("charts/funding/incomes_by_year.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: funding_incomes_by_year_and_scope
###########################################################################

def funding_incomes_by_year_and_scope(request, year, scope):
    path = '/charts/incomes_by_project/'

    project_incomes = []

    year_incomes = FundingAmount.objects.filter(year=year).order_by('own_amount')

    for year_income in year_incomes:
        funding = Funding.objects.get(id=year_income.funding_id)
        funding_program = FundingProgram.objects.get(id=funding.funding_program_id)
        project = Project.objects.get(id=funding.project_id)

        if funding_program.geographical_scope.name == scope:
            project_incomes.append({
                'short_name': project.short_name,
                'value': int(year_income.own_amount),
                'slug': project.slug,
            })

    project_incomes.insert(0, project_incomes.pop())

    # Another ordering type for pie slices
    # project_incomes.append(p_i[0])
    # length = len(p_i)
    # el = 2
    # if length > 1:
    #     for p in p_i[1:]:
    #         direction = 'left' if ( ( (length % 2 == 0) and (el % 2 == 0) ) or ( (length % 2 == 1) and (el % 2 == 1) ) ) else 'right'
    #         if direction == 'left':
    #             project_incomes.insert(0, p)
    #         else:
    #             project_incomes.append(p)
    #         el = el + 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'path': path,
        'project_incomes': project_incomes,
        'scope': scope,
        'year': year,
    }

    return render_to_response("charts/funding/incomes_by_year_and_scope.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: funding_incomes_by_project_index
###########################################################################

def funding_incomes_by_project_index(request):
    projects = Project.objects.all().order_by('slug')

    # dictionary to be returned in render_to_response()
    return_dict = {
        'projects': projects,
    }

    return render_to_response("charts/funding/incomes_by_project_index.html", return_dict, context_instance=RequestContext(request))


#########################
# View: funding_incomes_by_project
#########################

def funding_incomes_by_project(request, project_slug):
    project = Project.objects.get(slug=project_slug)

    funding_ids = Funding.objects.filter(project_id=project.id).values('id')

    project_incomes = FundingAmount.objects.filter(funding_id__in=funding_ids).values('year').annotate(total=Sum('own_amount'))

    # dictionary to be returned in render_to_response()
    return_dict = {
        'project': project,
        'project_incomes': project_incomes,
    }

    return render_to_response("charts/funding/incomes_by_project.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: funding_total_incomes_by_scope
###########################################################################

def funding_total_incomes_by_scope(request):
    incomes = {}

    geographical_scopes = GeographicalScope.objects.all()

    for geographical_scope in geographical_scopes:
        incomes[geographical_scope.name] = 0

    funding_amounts = FundingAmount.objects.all()

    min_year = FundingAmount.objects.aggregate(Min('year'))
    max_year = FundingAmount.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    incomes = {}

    for year in range(min_year, max_year + 1):
        incomes[year] = {}
        for scope in geographical_scopes:
            incomes[year][scope.name] = 0

    for funding_amount in funding_amounts:
        funding = Funding.objects.get(id=funding_amount.funding_id)
        funding_program = FundingProgram.objects.get(id=funding.funding_program.id)
        scope = funding_program.geographical_scope.name
        incomes[funding_amount.year][scope] = incomes[funding_amount.year][scope] + funding_amount.own_amount

    total_incomes = []

    current_year = date.today().year

    for year in range(min_year, max_year + 1):
        euskadi = int(incomes[year]['Euskadi'])
        spain = int(incomes[year]['Spain'])
        europe = int(incomes[year]['Europe'])
        certainty = False if (year > current_year) else True
        # total_incomes.append([year, euskadi, spain, europe, (euskadi+spain+europe), certainty])
        total_incomes.append({
            'year': year,
            'euskadi': euskadi,
            'spain': spain,
            'europe': europe,
            'total': (euskadi+spain+europe),
            'certainty': certainty,
        })

    # dictionary to be returned in render_to_response()
    return_dict = {
        'incomes': incomes,
        'total_incomes': total_incomes,
        'year': year,
    }

    return render_to_response("charts/funding/total_incomes_by_scope.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publications_number_of_publications
###########################################################################

def publications_number_of_publications(request):
    publications = {}

    publication_types = PublicationType.objects.all()

    # min_year = Publication.objects.aggregate(Min('published'))
    max_year = Publication.objects.aggregate(Max('published'))

    # min_year = min_year.get('published__min').year
    max_year = max_year.get('published__max').year

    min_year = 2000

    years = []
    for year in range(min_year, max_year + 1):
        years.append(year)

    for publication_type in publication_types:
        pub_type = publication_type.name.encode('utf-8')
        publications[pub_type] = {}
        for year in range(min_year, max_year + 1):
            publications[pub_type][year] = 0

    # all_publications = Publication.objects.all()
    all_publications = Publication.objects.all().exclude(authors=None)

    for publication in all_publications:
        pub_type = publication.publication_type.name.encode('utf-8')
        pub_year = publication.year
        if year in range(min_year, max_year + 1):
            publications[pub_type][pub_year] = publications[pub_type][pub_year] + 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'publication_types': publication_types,
        'publications': publications,
        'years': years,
    }

    return render_to_response("charts/publications/number_of_publications.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publications_coauthorship
###########################################################################

def publications_coauthorship(request, max_position=None):
    G = nx.Graph()

    pubs = Publication.objects.all()
    for pub in pubs:
        if max_position > 2:
            author_ids = PublicationAuthor.objects.filter(publication_id=pub.id).exclude(position__gt=max_position).values('author_id')
        else:
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

    G = nx_graph.analyze(G)

    data = json_graph.node_link_data(G)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'data': json.dumps(data),
    }

    return render_to_response("charts/publications/co_authorship.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publications_morelab_coauthorship
###########################################################################

def publications_morelab_coauthorship(request, max_position=None):
    G = nx.Graph()

    pubs = Publication.objects.all()
    for pub in pubs:
        if max_position > 2:
            author_ids = PublicationAuthor.objects.filter(publication_id=pub.id).exclude(position__gt=max_position).values('author_id')
        else:
            author_ids = PublicationAuthor.objects.filter(publication_id=pub.id).values('author_id')

        if author_ids:
            _list = [author_id['author_id'] for author_id in author_ids]
            for pos, author_id in enumerate(_list):
                for i in range(pos+1, len(_list)):
                    author = Person.objects.get(id=author_id)
                    author2 = Person.objects.get(id=_list[i])
                    if author.is_active and author2.is_active:
                        G.add_edge(author.id, author2.id)
                        try:
                            G[author.id][author2.id]['weight'] += 1
                        except:
                            G[author.id][author2.id]['weight'] = 1
                        G.node[author.id]['name'] = author.full_name
                        G.node[author2.id]['name'] = author2.full_name

    G = nx_graph.analyze(G)

    data = json_graph.node_link_data(G)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'data': json.dumps(data),
    }

    return render_to_response("charts/publications/co_authorship.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: projects_collaborations
###########################################################################

def projects_collaborations(request):
    G = nx.Graph()

    projects = Project.objects.all()
    pr_role = Role.objects.get(slug='principal-researcher')
    for project in projects:
        person_ids = AssignedPerson.objects.filter(project_id=project.id).exclude(role_id=pr_role.id).values('person_id')
        if person_ids:
            _list = [person_id['person_id'] for person_id in person_ids]
            for pos, person_id in enumerate(_list):
                for i in range(pos+1, len(_list)):
                    person1 = Person.objects.get(id=person_id)
                    person2 = Person.objects.get(id=_list[i])
                    G.add_edge(person1.id, person2.id)
                    try:
                        G[person1.id][person2.id]['weight'] += 1
                    except:
                        G[person1.id][person2.id]['weight'] = 1
                    G.node[person1.id]['name'] = person1.full_name
                    G.node[person2.id]['name'] = person2.full_name

    G = nx_graph.analyze(G)

    data = json_graph.node_link_data(G)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'data': json.dumps(data),
    }

    return render_to_response("charts/projects/collaboration.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: projects_morelab_collaborations
###########################################################################

def projects_morelab_collaborations(request):
    G = nx.Graph()

    projects = Project.objects.all()
    pr_role = Role.objects.get(slug='principal-researcher')
    for project in projects:
        person_ids = AssignedPerson.objects.filter(project_id=project.id).exclude(role_id=pr_role.id).values('person_id')
        if person_ids:
            _list = [person_id['person_id'] for person_id in person_ids]
            for pos, person_id in enumerate(_list):
                for i in range(pos+1, len(_list)):
                    person1 = Person.objects.get(id=person_id)
                    person2 = Person.objects.get(id=_list[i])
                    if person1.is_active and person2.is_active:
                        G.add_edge(person1.id, person2.id)
                        try:
                            G[person1.id][person2.id]['weight'] += 1
                        except:
                            G[person1.id][person2.id]['weight'] = 1
                        G.node[person1.id]['name'] = person1.full_name
                        G.node[person2.id]['name'] = person2.full_name

    G = nx_graph.analyze(G)

    data = json_graph.node_link_data(G)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'data': json.dumps(data),
    }

    return render_to_response("charts/projects/collaboration_morelab.html", return_dict, context_instance=RequestContext(request))
