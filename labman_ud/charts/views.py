# coding: utf-8

from itertools import combinations
from collections import defaultdict, OrderedDict
from datetime import date

# from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Min, Max
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from charts.utils import nx_graph
from networkx.readwrite import json_graph

from entities.funding_programs.models import FundingProgram
from entities.organizations.models import Organization
from entities.persons.models import Person, Job
from entities.projects.models import Project, FundingAmount, Funding, AssignedPerson
from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag
from entities.utils.models import GeographicalScope, Role

import json
import networkx as nx

from entities.persons.views import OWN_ORGANIZATION_SLUGS

# Create your views here.


###########################################################################
# View: chart_index
###########################################################################

def chart_index(request):
    return render_to_response('charts/index.html', {'web_title': 'Charts'})


###########################################################################
# View: funding_total_incomes
###########################################################################

def funding_total_incomes(request):
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
        certainty = False if (year >= current_year) else True
        incomes.append({'key': year, 'value': int(income['value']), 'certainty': certainty})

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'Total incomes',
        'incomes': incomes,
    }

    return render_to_response("charts/funding/total_incomes.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: funding_incomes_by_year
###########################################################################

def funding_incomes_by_year(request, year):
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
        'web_title': u'Total incomes by year',
        'incomes': incomes,
        'year': year,
    }

    return render_to_response("charts/funding/incomes_by_year.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: funding_incomes_by_year_and_scope
###########################################################################

def funding_incomes_by_year_and_scope(request, year, scope):
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
        'web_title': u'Total incomes by year and scope',
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
        'web_title': u'Total incomes by project index',
        'projects': projects,
    }

    return render_to_response("charts/funding/incomes_by_project_index.html", return_dict, context_instance=RequestContext(request))


#########################
# View: funding_incomes_by_project
#########################

def funding_incomes_by_project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    funding_ids = Funding.objects.filter(project_id=project.id).values('id')

    project_incomes = FundingAmount.objects.filter(funding_id__in=funding_ids).values('year').annotate(total=Sum('own_amount'))

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'Total incomes by project',
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
        certainty = False if (year >= current_year) else True
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
        'web_title': u'Total incomes by scope',
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
        if pub_year in range(min_year, max_year + 1):
            publications[pub_type][pub_year] = publications[pub_type][pub_year] + 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'Number of publications',
        'publication_types': publication_types,
        'publications': publications,
        'years': years,
    }

    return render_to_response("charts/publications/number_of_publications.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: projects_number_of_projects
###########################################################################

def projects_number_of_projects(request):
    geographical_scopes = GeographicalScope.objects.all()
    geographical_scopes_by_id = {}
    for geographical_scope in geographical_scopes:
        geographical_scopes_by_id[geographical_scope.id] = geographical_scope.name

    fundings = Funding.objects.all().select_related('project', 'funding_program')
    projects_data = defaultdict(lambda: defaultdict(set))
    # {
    #    year : {
    #        project_id : [ scope1, scope2, scope3 ]
    #    }
    #}

    scopes = set()

    for funding in fundings:
        for year in range(funding.project.start_year, funding.project.end_year + 1):
            projects_data[year][funding.project_id].add(geographical_scopes_by_id[funding.funding_program.geographical_scope_id])
            scopes.add(geographical_scopes_by_id[funding.funding_program.geographical_scope_id])

    years = sorted(projects_data.keys())

    projects = {}

    for scope in scopes:
        projects[scope] = OrderedDict()
        for year in years:
            projects[scope][year] = 0

    for year in years:
        for project_id in projects_data.get(year, []):
            for scope in projects_data[year][project_id]:
                projects[scope][year] += 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'Number of projects',
        'projects': projects,
        'years': years,
    }

    return render_to_response("charts/projects/number_of_projects.html", return_dict, context_instance=RequestContext(request))
    # return render_to_response("charts/publications/number_of_publications.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publications_coauthorship
###########################################################################

def publications_coauthorship(request, max_position=None):
    G = nx.Graph()

    if max_position and int(max_position) > 1:
        pub_authors = PublicationAuthor.objects.exclude(position__gt=max_position).values("publication_id", "author_id", "author_id__full_name")
    else:
        pub_authors = PublicationAuthor.objects.all().values("publication_id", "author_id", "author_id__full_name")

    authors_per_publication = defaultdict(list)  # 'publication_id' : [ pub_author1, pub_author2, pub_author3 ]

    for pub_author in pub_authors:
        entry = (pub_author['author_id'], pub_author['author_id__full_name'])
        authors_per_publication[pub_author['publication_id']].append(entry)

    for relations in authors_per_publication.values():
        for (author_id1, name1), (author_id2, name2) in combinations(relations, 2):
            G.add_edge(author_id1, author_id2)

            try:
                G[author_id1][author_id2]['weight'] += 1
            except:
                G[author_id1][author_id2]['weight'] = 1

            G.node[author_id1]['name'] = name1
            G.node[author_id2]['name'] = name2

    G = nx_graph.analyze(G)

    data = json_graph.node_link_data(G)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'Publications co-authorship',
        'data': json.dumps(data),
    }

    return render_to_response("charts/publications/co_authorship.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publications_morelab_coauthorship
###########################################################################

def publications_morelab_coauthorship(request, max_position=None):
    G = nx.Graph()

    if max_position and int(max_position) > 1:
        pub_authors = PublicationAuthor.objects.exclude(position__gt=max_position).values("publication_id", "author_id", "author_id__full_name")
    else:
        pub_authors = PublicationAuthor.objects.all().values("publication_id", "author_id", "author_id__full_name")

    people = Person.objects.all().values("is_active", "id")
    active_by_id = {}
    for person in people:
        active_by_id[person['id']] = person['is_active']

    authors_per_publication = defaultdict(list)  # 'publication_id' : [ pub_author1, pub_author2, pub_author3 ]

    for pub_author in pub_authors:
        if active_by_id[pub_author['author_id']]:
            entry = (pub_author['author_id'], pub_author['author_id__full_name'])
            authors_per_publication[pub_author['publication_id']].append(entry)

    for relations in authors_per_publication.values():
        for (author_id1, name1), (author_id2, name2) in combinations(relations, 2):
            G.add_edge(author_id1, author_id2)

            try:
                G[author_id1][author_id2]['weight'] += 1
            except:
                G[author_id1][author_id2]['weight'] = 1

            G.node[author_id1]['name'] = name1
            G.node[author_id2]['name'] = name2

    G = nx_graph.analyze(G)

    data = json_graph.node_link_data(G)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'Group publications co-authorship',
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
        'web_title': u'Collaborations',
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
        'web_title': u'Group collaborations',
        'data': json.dumps(data),
    }

    return render_to_response("charts/projects/collaboration_morelab.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publications_egonetwork
###########################################################################

def publications_egonetwork(request, author_slug):
    author = get_object_or_404(Person, slug=author_slug)

    G = nx.Graph()

    pub_authors = PublicationAuthor.objects.all().values("publication_id", "author_id", "author_id__full_name")

    authors_per_publication = defaultdict(list)  # 'publication_id' : [ pub_author1, pub_author2, pub_author3 ]

    for pub_author in pub_authors:
        entry = (pub_author['author_id'], pub_author['author_id__full_name'])
        authors_per_publication[pub_author['publication_id']].append(entry)

    for relations in authors_per_publication.values():
        for (author_id1, name1), (author_id2, name2) in combinations(relations, 2):
            G.add_edge(author_id1, author_id2)

            try:
                G[author_id1][author_id2]['weight'] += 1
            except:
                G[author_id1][author_id2]['weight'] = 1

            G.node[author_id1]['name'] = name1
            G.node[author_id2]['name'] = name2

    try:
        G = nx_graph.analyze(G)
        ego_g = nx.ego_graph(G, author.id)
        data = json_graph.node_link_data(ego_g)
    except:
        data = {}

    # dictionary to be returned in render_to_response()
    return_dict = {
        # 'publication_tags_per_year': publication_tags_per_year,
        'web_title': u'%s - Egonetwork' % author.full_name,
        'data': json.dumps(data),
        'author': author,
    }

    return render_to_response("charts/publications/egonetwork.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publications_by_author
###########################################################################

def publications_by_author(request, author_slug):
    publications = {}
    publication_types = PublicationType.objects.all()

    author = get_object_or_404(Person, slug=author_slug)

    publication_ids = PublicationAuthor.objects.filter(author=author.id).values('publication_id')
    _publications = Publication.objects.filter(id__in=publication_ids)

    min_year = _publications.aggregate(Min('year'))
    max_year = _publications.aggregate(Max('year'))

    max_year = date.today().year
    # At least 7 years must be provided (even if they're 0) to
    # have a nice graph in nvd3. Otherwise, years are repeated in
    # people who published lately
    min_year = min(max_year - 7, min_year.get('year__min'))

    years = []

    for year in range(min_year, max_year + 1):
        years.append(year)

    for publication_type in publication_types:
        pub_type = publication_type.name.encode('utf-8')
        publications[pub_type] = {}
        for year in range(min_year, max_year + 1):
            publications[pub_type][year] = 0

    for publication in _publications:
        pub_type = publication.publication_type.name.encode('utf-8')
        pub_year = publication.year
        if pub_year in range(min_year, max_year + 1):
            publications[pub_type][pub_year] = publications[pub_type][pub_year] + 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'%s - Number of publications' % author.full_name,
        'author': author,
        'publication_types': publication_types,
        'publications': publications,
        'years': years,
    }

    return render_to_response("charts/publications/number_of_publications_by_author.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: tags_by_author
###########################################################################

def tags_by_author(request, author_slug):
    tag_dict = {}

    author = get_object_or_404(Person, slug=author_slug)

    publication_ids = PublicationAuthor.objects.filter(author=author.id).values('publication_id')
    tags = PublicationTag.objects.filter(publication_id__in=publication_ids)

    for tag in tags:
        t = tag.tag.name
        if t in tag_dict.keys():
            tag_dict[t] = tag_dict[t] + 1
        else:
            tag_dict[t] = 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'%s - Tag cloud' % author.full_name,
        'author': author,
        'tag_dict': tag_dict,
    }

    return render_to_response('charts/publications/tags_by_author.html', return_dict, context_instance=RequestContext(request))

###########################################################################
# View: group_timeline
###########################################################################

def cmp_members_by_start_date(member1, member2):
    for field in 'start_year', 'start_month', 'end_year', 'end_month':
        if member1[field] != member2[field]:
            return cmp(member1[field], member2[field])

    return 0

def cmp_members_by_current_date(member1, member2):
    for field in 'end_year', 'end_month':
        if member1[field] != member2[field]:
            return cmp(member2[field], member1[field])

    for field in 'start_year', 'start_month':
        if member1[field] != member2[field]:
            return cmp(member1[field], member2[field])


    return 0

def cmp_members_by_length_current_first(member1, member2):
    if member1['current'] != member2['current']:
        if member1['current']:
            return -1
        else:
            return 1
    
    return cmp(member2['length'], member1['length'])

def recursively(result, time_together_per_member, already_processed, member):
    for current_element, days in time_together_per_member[member]:
        if current_element not in already_processed:
            result.append(current_element)
            already_processed.add(current_element)
            recursively(result, time_together_per_member, already_processed, current_element)

def sort_members_by_together_time(members):
    members_by_member = {}
    max_length = 0
    max_member = None
    for member in members:
        members_by_member[member['member']] = member
        if member['length'].days > max_length:
            max_length = member['length'].days
            max_member = member['member']

    # Build dictionary such as
    time_together_per_member = OrderedDict()
        # member1 : [ (member2, 15), (member3, 10) ...] # Sorted by days_together
    
    sorted_member_info = sorted(members, lambda m1, m2 : cmp(m2['length'], m1['length']))
    sorted_members = map(lambda x : x['member'], sorted_member_info)

    members_per_day_together = defaultdict(list)
        # 315 : [('a','b'), ('a','c'), ('d','e')],

    for member1 in sorted_member_info:
        time_together_per_member[member1['member']] = []

        for member2 in members:
            if member1 == member2:
                continue

            max_start = max(member1['start'], member2['start'])
            min_end = min(member1['end'], member2['end'])
            if max_start > min_end:
                days_together = 0
            else:
                days_together = (min_end - max_start).days
            
            if days_together:
                time_together_per_member[member1['member']].append( (member2['member'], days_together ))
                members_per_day_together[days_together].append( (member1['member'], member2['member']))

        time_together_per_member[member1['member']].sort(lambda (m1, d1), (m2, d2) : cmp(d2, d1))
    
    already_processed = set([max_member])

    sorted_list = [max_member]
    recursively(sorted_list, time_together_per_member, already_processed, max_member)

    if False:
        for key in sorted(members_per_day_together, reverse = True):
            for member1, member2 in members_per_day_together[key]:
                if member1 not in already_processed:
                    sorted_list.append(member1)
                    already_processed.add(member1)

                if member2 not in already_processed:
                    sorted_list.append(member2)
                    already_processed.add(member2)

    return map(lambda x : members_by_member[x], sorted_list)


def group_timeline(request):
    organizations = Organization.objects.filter(slug__in=OWN_ORGANIZATION_SLUGS)
    member_ids = Job.objects.filter(organization__in=organizations).values('person_id')
    member_list = Person.objects.filter(id__in=member_ids).select_related('jobs')
    members = []
    for member in member_list:
        jobs = Job.objects.filter(person_id=member.id, organization_id__in=organizations).order_by('end_date')
        first_job = jobs[0]
        if first_job.start_date is None:
            print "Skipping", member.full_name
            continue

        record = {
            'member' : member, 
            'start_year' : first_job.start_date.year, 
            'start_month' : first_job.start_date.month,
            'start' : first_job.start_date,
        }
        last_job = jobs.reverse()[0]

        if last_job.end_date is not None:
            record.update({
                'end_year' : last_job.end_date.year, 
                'end_month' : last_job.end_date.month,
                'end' : last_job.end_date,
                'length' : last_job.end_date - first_job.start_date,
                'current' : False,
            })
        else:
            today = date.today()
            record.update({
                'end_year' : today.year, 
                'end_month' : today.month,
                'end' : today,
                'length' : today - first_job.start_date,
                'current' : True,
            })
        members.append(record)

    algorithms = {
        0 : cmp_members_by_start_date,
        1 : cmp_members_by_current_date,
        2 : cmp_members_by_length_current_first,
        3 : sort_members_by_together_time
    }
    sort_algorithm = request.GET.get('sort', 0)
    try:
        sort_algorithm_number = int(sort_algorithm)
        if sort_algorithm_number >= len(algorithms):
            sort_algorithm_number = 0
    except:
        sort_algorithm_number = 0
    
    if sort_algorithm_number in [3]:
        members = algorithms[sort_algorithm_number](members)
    else:
        members.sort(algorithms[sort_algorithm_number])

    return_dict = {
        'members' : members,
        'chart_height' : len(members) * 50,
    }
    return render_to_response('charts/people/group_timeline.html', return_dict, context_instance=RequestContext(request))
