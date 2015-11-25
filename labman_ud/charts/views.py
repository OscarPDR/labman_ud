# -*- encoding: utf-8 -*-

from itertools import combinations
from collections import defaultdict, OrderedDict
import datetime
import operator

# from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Min, Max
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify

from charts.utils import nx_graph
from networkx.readwrite import json_graph

from entities.funding_programs.models import *
from entities.organizations.models import *
from entities.persons.models import *
from entities.projects.models import *
from entities.publications.models import *
from entities.utils.models import *
from entities.projects.utils import *

from labman_setup.models import *

import inflection
import json
import networkx as nx
import numpy as np
from collections import OrderedDict, Counter


UNIT_ORGANIZATION_IDS = Unit.objects.all().values_list('organization', flat=True)

PUBLICATION_TYPES = {
    'BookSection' : 'Book section',
    'Book' : 'Book',
    'ConferencePaper' : 'Conference paper',
    'Proceedings' : 'Proceedings',
    'JournalArticle' : 'Journal article',
    'JCR' : 'JCR indexed journal article',
    'Journal' : 'Journal',
    'MagazineArticle' : 'Magazine article',
    'Magazine' : 'Magazine',
    'Thesis' : 'PhD dissertation'
}

PUBLICATION_COLORS = {
    'BookSection' : '#ffaaaa',
    'ConferencePaper' : '#ffecaa',
    'JournalArticle' : '#88cc88',
    'MagazineArticle' : '#827fb2',
}


####################################################################################################
###     chart_index
####################################################################################################

def chart_index(request):
    return render(request, 'charts/index.html', {'web_title': 'Charts'})


####################################################################################################
###     funding_total_incomes
####################################################################################################

def funding_total_incomes(request):
    min_year = FundingAmount.objects.aggregate(Min('year'))
    max_year = FundingAmount.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    incomes = []

    current_year = datetime.date.today().year

    for year in range(min_year, max_year + 1):
        income = FundingAmount.objects.filter(year=year).aggregate(value=Sum('own_amount'))
        if income['value'] is None:
            income['value'] = 0
        certainty = False if (year >= current_year) else True
        incomes.append({'key': year, 'value': int(income['value']), 'certainty': certainty})

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Total incomes',
        'incomes': incomes,
    }

    return render(request, "charts/funding/total_incomes.html", return_dict)


####################################################################################################
###     funding_incomes_by_year
####################################################################################################

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

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Total incomes by year',
        'incomes': incomes,
        'year': year,
    }

    return render(request, "charts/funding/incomes_by_year.html", return_dict)


####################################################################################################
###     funding_incomes_by_year_and_scope
####################################################################################################

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

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Total incomes by year and scope',
        'project_incomes': project_incomes,
        'scope': scope,
        'year': year,
    }

    return render(request, "charts/funding/incomes_by_year_and_scope.html", return_dict)


####################################################################################################
###     funding_incomes_by_project_index
####################################################################################################

def funding_incomes_by_project_index(request):
    projects = Project.objects.all().order_by('slug')

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Total incomes by project index',
        'projects': projects,
    }

    return render(request, "charts/funding/incomes_by_project_index.html", return_dict)


####################################################################################################
###     funding_incomes_by_project
####################################################################################################

def funding_incomes_by_project(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    funding_ids = Funding.objects.filter(project_id=project.id).values('id')

    project_incomes = FundingAmount.objects.filter(funding_id__in=funding_ids).values('year').annotate(total=Sum('own_amount'))

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Total incomes by project',
        'project': project,
        'project_incomes': project_incomes,
    }

    return render(request, "charts/funding/incomes_by_project.html", return_dict)


####################################################################################################
###     funding_total_incomes_by_scope
####################################################################################################

def funding_total_incomes_by_scope(request):

    geographical_scopes = GeographicalScope.objects.all().order_by('slug')

    geographical_scope_names = []

    for scope in geographical_scopes:
        geographical_scope_names.append(str(scope.name))

    min_year = FundingAmount.objects.aggregate(Min('year')).get('year__min')
    max_year = FundingAmount.objects.aggregate(Max('year')).get('year__max')
    current_year = datetime.date.today().year

    incomes = {}

    for year in range(min_year, max_year + 1):
        incomes[year] = {}

        for scope in geographical_scopes:
            incomes[year][scope.name] = 0

    for funding_amount in FundingAmount.objects.all():
        scope = funding_amount.funding.funding_program.geographical_scope.name

        if funding_amount.year in range(min_year, max_year + 1):
            incomes[funding_amount.year][scope] = incomes[funding_amount.year][scope] + funding_amount.own_amount

    total_incomes = []

    for year in range(min_year, max_year + 1):
        income_item = [str(year)]

        total = 0
        certainty = False if (year >= current_year) else True

        for scope in geographical_scopes:
            income_for_year_and_scope = int(incomes[year][str(scope.name)])
            income_item.append(income_for_year_and_scope)
            income_item.append(certainty)

            total += income_for_year_and_scope

        income_item.append(total)
        income_item.append(certainty)

        total_incomes.append(income_item)

    return_dict = {
        'web_title': u'Total incomes by scope',
        'total_incomes': total_incomes,
        'geographical_scope_names': geographical_scope_names,
    }

    return render(request, "charts/funding/total_incomes_by_scope.html", return_dict)


###     publications_number_of_publications()
####################################################################################################

def publications_number_of_publications(request):

    min_year = 2000
    max_year = datetime.datetime.now().year + 1

    years = []

    for year in range(min_year, max_year):
        years.append(year)

    default_pub_dict = {}
    totals_by_year = {}

    authored_publications = Publication.objects.all().exclude(authors=None)
    authored_publications = authored_publications.select_related('journalarticle', 'journalarticle__parent_journal')

    publication_types = list(set(authored_publications.values_list('child_type', flat=True)))
    publication_types.append('JCR')

    for pub_type in publication_types:
        default_pub_dict[pub_type] = {}
        for year in range(min_year, max_year):
            default_pub_dict[pub_type][year] = 0
            totals_by_year[year] = 0

    for authored_pub in authored_publications:
        pub_type = authored_pub.child_type
        if (pub_type == 'JournalArticle') and (authored_pub.journalarticle.parent_journal.impact_factor):
            pub_type = 'JCR'

        pub_year = authored_pub.year
        if pub_year in range(min_year, max_year):
            default_pub_dict[pub_type][pub_year] = default_pub_dict[pub_type][pub_year] + 1
            totals_by_year[pub_year] = totals_by_year.get(pub_year, 0) + 1

    publication_counts = [{
        'key': 'Total',
        'values': [{'x': year, 'y': count} for year, count in totals_by_year.iteritems()]
    }]

    for pub_type, value_dict in default_pub_dict.iteritems():
        item_dict = {
            'key': str(inflection.titleize(pub_type)),
            'values': []
        }
        for year, count in value_dict.iteritems():
            item_dict['values'].append({'x': year, 'y': count})

        publication_counts.append(item_dict)

    return_dict = {
        'web_title': u'Number of publications',
        'publication_counts': publication_counts,
        'years': years,
    }

    return render(request, "charts/publications/number_of_publications.html", return_dict)


###     projects_number_of_projects()
####################################################################################################

def projects_number_of_projects(request):

    geographical_scopes_by_id = {}

    for geographical_scope in GeographicalScope.objects.all():
        geographical_scopes_by_id[geographical_scope.id] = geographical_scope.name

    fundings = Funding.objects.all().select_related('project', 'funding_program')
    projects_data = defaultdict(lambda: defaultdict(set))
    # {
    #    year: {
    #        project_id: [ scope1, scope2, scope3 ]
    #    }
    # }

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

    return_dict = {
        'web_title': u'Number of projects',
        'projects': projects,
        'years': years,
    }

    return render(request, "charts/projects/number_of_projects.html", return_dict)


####################################################################################################
###     publication_coauthorships
####################################################################################################

def publication_coauthorships(request, max_position=None, within_group=False):

    G = nx.Graph()

    if max_position and int(max_position) > 1:
        pub_authors = PublicationAuthor.objects.exclude(position__gt=max_position)

    else:
        pub_authors = PublicationAuthor.objects.all()

    pub_authors = pub_authors.values("publication_id", "author_id", "author_id__full_name")

    # 'publication_id': [ pub_author1, pub_author2, pub_author3 ]
    authors_per_publication = defaultdict(list)

    if within_group:
        people = Person.objects.all().values("is_active", "id")
        active_by_id = {}

        for person in people:
            active_by_id[person['id']] = person['is_active']

    for pub_author in pub_authors:
        check_coauthorship = True

        if within_group and not active_by_id[pub_author['author_id']]:
            check_coauthorship = False

        if check_coauthorship:
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

    return_dict = {
        'data': json.dumps(data),
        'web_title': u'Publications co-authorship',
        'within_group': within_group,
    }

    return render(request, "charts/publications/co_authorship.html", return_dict)


####################################################################################################
###     project_collaborations
####################################################################################################

def project_collaborations(request, exclude_leaders=False, within_group=False):

    G = nx.Graph()

    projects = Project.objects.all()

    for project in projects:
        if exclude_leaders:
            person_ids = AssignedPerson.objects.filter(
                    project=project
                ).exclude(
                    role__exclude_from_charts=True
                ).values_list('person_id', flat=True)
        else:
            person_ids = AssignedPerson.objects.filter(
                    project=project
                ).values_list('person_id', flat=True)

        if person_ids:
            for pos, person_id in enumerate(person_ids):
                for i in range(pos+1, len(person_ids)):
                    person1 = Person.objects.get(id=person_id)
                    person2 = Person.objects.get(id=person_ids[i])

                    add_node = True

                    if within_group and (not person1.is_active or not person2.is_active):
                        add_node = False

                    if add_node:
                        G.add_edge(person1.id, person2.id)

                        try:
                            G[person1.id][person2.id]['weight'] += 1
                        except:
                            G[person1.id][person2.id]['weight'] = 1

                        G.node[person1.id]['name'] = person1.full_name
                        G.node[person2.id]['name'] = person2.full_name

    G = nx_graph.analyze(G)

    data = json_graph.node_link_data(G)

    return_dict = {
        'data': json.dumps(data),
        'web_title': u'Group collaborations',
        'within_group': within_group,
    }

    return render(request, "charts/projects/collaboration.html", return_dict)


####################################################################################################
###     publications_egonetwork
####################################################################################################

def publications_egonetwork(request, author_slug):
    author = get_object_or_404(Person, slug=author_slug)

    G = nx.Graph()

    pub_authors = PublicationAuthor.objects.all().values("publication_id", "author_id", "author_id__full_name")

    authors_per_publication = defaultdict(list)  # 'publication_id': [ pub_author1, pub_author2, pub_author3 ]

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

    # dictionary to be returned in render(request, )
    return_dict = {
        # 'publication_tags_per_year': publication_tags_per_year,
        'web_title': u'%s - Egonetwork' % author.full_name,
        'data': json.dumps(data),
        'author': author,
    }

    return render(request, "charts/publications/egonetwork.html", return_dict)


####################################################################################################
###     publications_by_author
####################################################################################################

def publications_by_author(request, author_slug):
    publications = {}

    author = get_object_or_404(Person, slug=author_slug)

    publication_ids = PublicationAuthor.objects.filter(author=author.id).values('publication_id')
    _publications = Publication.objects.select_related('journalarticle', 'journalarticle__parent_journal').filter(id__in=publication_ids)

    min_year = _publications.aggregate(Min('year'))
    max_year = _publications.aggregate(Max('year'))

    max_year = datetime.date.today().year
    min_year = min_year.get('year__min')
    # At least 7 years must be provided (even if they're 0) to
    # have a nice graph in nvd3. Otherwise, years are repeated in
    # people who published lately
    if min_year:
        min_year = min(max_year - 7, min_year)
    else:
        min_year = max_year - 7

    years = []

    for year in range(min_year, max_year + 1):
        years.append(year)

    for publication_type in PUBLICATION_TYPES:
        publications[publication_type] = {}
        for year in range(min_year, max_year + 1):
            publications[publication_type][year] = 0

    for publication in _publications:
        pub_type = publication.child_type
        if pub_type == 'JournalArticle':
            if publication.journalarticle.parent_journal.impact_factor:
                pub_type = 'JCR'

        pub_year = publication.year
        if pub_year in range(min_year, max_year + 1):
            publications[pub_type][pub_year] = publications[pub_type][pub_year] + 1

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'%s - Number of publications' % author.full_name,
        'author': author,
        'publication_types': PUBLICATION_TYPES,
        'publications': publications,
        'years': years,
    }

    return render(request, "charts/publications/number_of_publications_by_author.html", return_dict)


####################################################################################################
###     publication_places_by_author(author_slug, child_type=None)
####################################################################################################

def publication_places_by_author(request, author_slug, child_type=None):

    author = get_object_or_404(Person, slug=author_slug)

    place_set = set()

    pub_types = set()

    for publication in PublicationAuthor.objects.filter(author=author):
        pub_types.add(str(publication.publication.child_type))

    pub_types = sorted(list(pub_types))

    colors = []

    max_value = 0

    full_list = []

    ###     child_type
    ###########################################################################
    if child_type:
        min_year = PublicationAuthor.objects.filter(author=author).aggregate(Min('publication__year'))
        min_year = min_year.get('publication__year__min')
        max_year = datetime.date.today().year

        colors = None

        publications = PublicationAuthor.objects.filter(author=author, publication__child_type=child_type)

        for publication in publications:
            place_set.add(publication.position)

        place_list = sorted(list(place_set))
        place_list = [str(place) + _author_place_suffix(place) for place in place_list]

        full_list.append(['year'] + place_list + ['Total'])

        list_length = len(place_list)

        for year in range(min_year, max_year + 1):
            inner_list = [0] * (len(place_list) + 2)
            inner_list[0] = str(year)

            for filtered_publication in publications.filter(publication__year=year):
                place_str = str(filtered_publication.position) + _author_place_suffix(filtered_publication.position)
                index = place_list.index(place_str) + 1
                inner_list[index] += 1
                inner_list[-1] += 1

            if inner_list[-1] > max_value:
                max_value = inner_list[-1]

            full_list.append(inner_list)

    else:
        publications = PublicationAuthor.objects.filter(author=author)

        for publication in publications:
            place_set.add(publication.position)

        place_list = sorted(list(place_set))

        for pub_type in pub_types:
            if pub_type in PUBLICATION_COLORS:
                colors.append(PUBLICATION_COLORS[pub_type])

        full_list.append(['place'] + pub_types + ['Total'])

        list_length = len(pub_types)

        for place in place_list:
            inner_list = [0] * (len(pub_types) + 2)
            inner_list[0] = str(place) + _author_place_suffix(place)

            for filtered_publication in publications.filter(position=place):
                index = pub_types.index(filtered_publication.publication.child_type) + 1
                inner_list[index] += 1
                inner_list[-1] += 1

            if inner_list[-1] > max_value:
                max_value = inner_list[-1]

            full_list.append(inner_list)

    ###     end child_type
    ###########################################################################

    ROUND_TO = 5 if (max_value > 5) else 3
    max_value = (max_value + ROUND_TO) / ROUND_TO * ROUND_TO

    return_dict = {
        'author': author,
        'child_type': child_type,
        'colors': colors,
        'len': list_length,
        'max_value': max_value,
        'pub_types': pub_types,
        'publication_places': full_list,
    }

    return render(request, "charts/publications/number_of_publications_by_place.html", return_dict)


def _author_place_suffix(place):

    suffixes = {
        1: 'st',
        2: 'nd',
        3: 'rd',
        21: 'st',
        22: 'nd',
        23: 'rd',
    }

    if place in suffixes.keys():
        return suffixes[place]

    else:
        return 'th'


####################################################################################################
###     group_timeline
####################################################################################################

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

    sorted_member_info = sorted(members, lambda m1, m2: cmp(m2['length'], m1['length']))
    # sorted_members = map(lambda x: x['member'], sorted_member_info)

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
                time_together_per_member[member1['member']].append((member2['member'], days_together))
                members_per_day_together[days_together].append((member1['member'], member2['member']))

        time_together_per_member[member1['member']].sort(lambda (m1, d1), (m2, d2): cmp(d2, d1))

    already_processed = set([max_member])

    sorted_list = [max_member]
    recursively(sorted_list, time_together_per_member, already_processed, max_member)

    if False:
        for key in sorted(members_per_day_together, reverse=True):
            for member1, member2 in members_per_day_together[key]:
                if member1 not in already_processed:
                    sorted_list.append(member1)
                    already_processed.add(member1)

                if member2 not in already_processed:
                    sorted_list.append(member2)
                    already_processed.add(member2)

    return map(lambda x: members_by_member[x], sorted_list)

VERY_NEW_DATE = date(2100, 1, 1)


def group_timeline(request):
    organizations = Organization.objects.filter(id__in=UNIT_ORGANIZATION_IDS)
    member_jobs = Job.objects.filter(organization__in=organizations).select_related('person', 'organization')
    jobs_by_member = defaultdict(list)
    for member_job in member_jobs:
        jobs_by_member[member_job.person].append(member_job)

    for member in jobs_by_member:
        jobs_by_member[member].sort(lambda j1, j2: cmp(j1.end_date or VERY_NEW_DATE, j2.end_date or VERY_NEW_DATE))

    members = []
    members_by_id = {}
    for member, jobs in jobs_by_member.iteritems():
        # jobs = Job.objects.filter(person_id=member.id, organization_id__in=organizations).order_by('end_date')
        first_job = jobs[0]
        if first_job.start_date is None:
            continue

        last_job = jobs[-1]
        record = {
            'member': member.full_name,
            'organization': last_job.organization,
            'start_year': first_job.start_date.year,
            'start_month': first_job.start_date.month - 1,
            'start': first_job.start_date,
        }

        if last_job.end_date is not None:
            record.update({
                'end_year': last_job.end_date.year,
                'end_month': last_job.end_date.month - 1,
                'end': last_job.end_date,
                'length': last_job.end_date - first_job.start_date,
                'current': False,
            })
        else:
            today = datetime.date.today()
            record.update({
                'end_year': today.year,
                'end_month': today.month - 1,
                'end': today,
                'length': today - first_job.start_date,
                'current': True,
            })
        members.append(record)
        members_by_id[record['member']] = record

    algorithms = OrderedDict()
    algorithms['Last out, active first'] = cmp_members_by_current_date
    algorithms['Chronological'] = cmp_members_by_start_date
    algorithms['Duration, active first'] = cmp_members_by_length_current_first
    algorithms['Colleagues'] = sort_members_by_together_time
    sort_algorithm = request.GET.get('sort', algorithms.keys()[0])
    if sort_algorithm not in algorithms:
        sort_algorithm = algorithms.keys()[0]

    if sort_algorithm in ['Colleagues']:
        members = algorithms[sort_algorithm](members)
    else:
        members.sort(algorithms[sort_algorithm])

    units = []
    for member in members:
        units.append(member['organization'].short_name)

    return_dict = {
        'members': members,
        'chart_height': (len(members) + 1) * 50,
        'units': units,
        'distinct_units': sorted(set(units)),
        'algorithms': algorithms.keys(),
        'current_algorithm': sort_algorithm,
    }
    return render(request, 'charts/people/group_timeline.html', return_dict)


####################################################################################################
###     members_position_pie
####################################################################################################

def members_position_pie(request):
    organizations = Organization.objects.filter(slug__in=UNIT_ORGANIZATION_IDS)
    member_jobs = Job.objects.filter(organization__in=organizations, person__is_active=True).select_related('person', 'organization')

    jobs_by_member = defaultdict(list)
    for member_job in member_jobs:
        if member_job.person.is_active:
            jobs_by_member[member_job.person].append(member_job)

    positions = {}
    positions_per_organization = {}
    for member in jobs_by_member:
        jobs_by_member[member].sort(lambda j1, j2: cmp(j1.end_date or VERY_NEW_DATE, j2.end_date or VERY_NEW_DATE))
        last_organization = jobs_by_member[member][-1].organization.short_name
        last_position = jobs_by_member[member][-1].position.lower().title()
        if last_position not in positions:
            positions[last_position] = 1
        else:
            positions[last_position] += 1

        if last_organization not in positions_per_organization:
            positions_per_organization[last_organization] = {}
        if last_position not in positions_per_organization[last_organization]:
            positions_per_organization[last_organization][last_position] = 1
        else:
            positions_per_organization[last_organization][last_position] += 1

    return_dict = {
        'multiple_organizations': len(positions_per_organization) > 1,
        'positions_per_organization': positions_per_organization,
        'positions': positions,
    }

    return render(request, 'charts/people/pie.html', return_dict)


####################################################################################################
###     person_timeline
####################################################################################################

def person_timeline(request, person_slug):
    person = get_object_or_404(Person, slug=person_slug)

    jobs = Job.objects.filter(person=person).order_by('start_date')

    return_dict = {
        'person': person,
        'jobs': jobs,
        'chart_height': (len(jobs) + 1) * 50,
    }

    return render(request, 'charts/people/person_timeline.html', return_dict)


####################################################################################################
###     projects_timeline
####################################################################################################

def projects_timeline(request, person_slug):
    person = get_object_or_404(Person, slug=person_slug)

    projects_timeline = []
    role_colors = []
    role_items = OrderedDict()

    assigned_persons = AssignedPerson.objects.filter(
            person=person
        ).exclude(
            role__exclude_from_charts=True,
        ).order_by(
            'project__start_year',
            'project__start_month',
            'project__end_year',
            'project__end_month'
        )

    for assigned_person in assigned_persons:
        project = assigned_person.project

        timeline_item = {
            'short_name': project.short_name,
            'start_date': get_person_start_date(assigned_person),
            'end_date': get_person_end_date(assigned_person),
            'role': assigned_person.role.name,
        }

        if timeline_item['end_date'] > timeline_item['start_date']:
            projects_timeline.append(timeline_item)

        rgb_color = assigned_person.role.rgb_color

        if rgb_color and rgb_color not in role_colors:
            role_colors.append(str(rgb_color))

        role_items[assigned_person.role.name] = role_items.get(assigned_person.role.name, 0) + 1

    role_colors = list(role_colors) if len(role_colors) > 0 else None

    return_dict = {
        'chart_height': (len(projects_timeline) + 1) * 50,
        'person': person,
        'projects_timeline': projects_timeline,
        'role_colors': role_colors,
        'role_items': role_items,
        'roles': Role.objects.all(),
    }

    return render(request, 'charts/people/projects_timeline.html', return_dict)


####################################################################################################
###     gender_distribution
####################################################################################################

def gender_distribution(request, organization_slug=None):

    gender_distribution = {}
    gender_distribution_sets = {}

    min_year = 2005
    actual_year = datetime.date.today().year

    for year in range(min_year, actual_year + 1):
        gender_distribution[year] = {
            'female': 0,
            'male': 0,
        }
        gender_distribution_sets[year] = {
            'male': set(),
            'female': set(),
        }

    units = Unit.objects.all()
    organization = None

    if organization_slug:
        organization = get_object_or_404(Organization, slug=organization_slug)
        jobs = Job.objects.filter(organization=organization)
    else:
        jobs = Job.objects.all()

    for job in jobs:
        if job.start_date:
            start_year = job.start_date.year

            if start_year >= min_year:
                end_year = job.end_date.year if job.end_date else actual_year

                gender = job.person.gender.lower() if job.person.gender else 'male'

                for year in range(start_year, end_year + 1):
                    gender_distribution_sets[year][gender].add(job.person.full_name)

    max_persons = 0

    for year in range(min_year, actual_year + 1):
        gender_distribution[year]['female'] = len(gender_distribution_sets[year]['female'])
        gender_distribution[year]['male'] = len(gender_distribution_sets[year]['male'])
        total_year = gender_distribution[year]['female'] + gender_distribution[year]['male']
        if (total_year > max_persons):
            max_persons = total_year

    return_dict = {
        'gender_distribution': gender_distribution,
        'max_persons': max_persons,
        'units': units,
        'organization': organization,
    }

    return render(request, 'charts/people/gender_distribution.html', return_dict)


####################################################################################################
###     position_distribution
####################################################################################################

def position_distribution(request, organization_slug=None):

    position_distribution = {}
    position_distribution_sets = {}

    units = Unit.objects.all()
    organization = None

    if organization_slug:
        organization = get_object_or_404(Organization, slug=organization_slug)
        jobs = Job.objects.filter(organization=organization)
    else:
        jobs = Job.objects.all()

    position_list = jobs.values_list('position', flat=True)
    position_set = set()

    for position in position_list:
        position_set.add(position.capitalize())

    position_list = list(position_set)

    if '' in position_list:
        position_list.remove('')

    min_year = 2005
    actual_year = datetime.date.today().year

    for year in range(min_year, actual_year + 1):
        position_distribution[year] = {}
        position_distribution_sets[year] = {}

        for position in position_list:
            position_slug = slugify(position)
            position_distribution[year][position_slug] = 0
            position_distribution_sets[year][position_slug] = set()

    for job in jobs:
        if job.start_date:
            start_year = job.start_date.year

            if start_year >= min_year:
                end_year = job.end_date.year if job.end_date else actual_year

                position_slug = slugify(job.position)

                if position_slug != '':
                    for year in range(start_year, end_year + 1):
                        position_distribution_sets[year][position_slug].add(job.person.full_name)

    max_persons = 0

    for year in range(min_year, actual_year + 1):
        total_year = 0

        for position in position_list:
            position_slug = slugify(position)
            total_year = total_year + len(position_distribution_sets[year][position_slug])
            position_distribution[year][position_slug] = len(position_distribution_sets[year][position_slug])

        if (total_year > max_persons):
            max_persons = total_year

    position_distribution_array = []

    position_distribution_array.append(['Year'])

    for position in position_list:
        position_distribution_array[0].append(str(position))

    for year in range(min_year, actual_year + 1):
        array_row = [str(year)]
        for position in position_list:
            array_row.append(position_distribution[year][slugify(position)])

        position_distribution_array.append(array_row)

    return_dict = {
        'position_distribution_array': position_distribution_array,
        'max_persons': max_persons,
        'units': units,
        'organization': organization,
    }

    return render(request, 'charts/people/position_distribution.html', return_dict)


####################################################################################################
###     related_persons
####################################################################################################

def _calculate_relation_coefficient(s1, s2):
    inter_len = float(len(s1.intersection(s2)))
    current_len = len(s1)

    if current_len > 0:
        coef = inter_len / current_len
    else:
        coef = 0

    return coef


def related_persons(request, person_slug, top):

    publication_tags = defaultdict(list)
        # pub_id : tags
    # }

    persons_dict = {
        # person__full_name : {
        #      'tag_name' : N # number of times for this person
        # }
    }

    for pub_tag in PublicationTag.objects.all().select_related('tag__name').values('publication', 'tag__name'):
        publication_tags[pub_tag['publication']].append(pub_tag['tag__name'])

    for pub_author in PublicationAuthor.objects.all().select_related('author__full_name').values('author__full_name', 'publication'):
        name = pub_author['author__full_name']
        if name not in persons_dict:
            persons_dict[name] = {}

        cur_dict = persons_dict[name]

        for tag in publication_tags.get(pub_author['publication'], []):
            if tag in cur_dict:
                cur_dict[tag] += 1
            else:
                cur_dict[tag] = 1

    for person in persons_dict:
        cur_dict = persons_dict[person]

        # We only take into account the 50% most significant tags
        # It can happen that someone doesn't have any significant tags ([1, 1, 1, 1])
        values = [cur_dict[e] for e in cur_dict]
        if values:
            limit = np.percentile(values, 50)

            significant_tags = {}
            for tag in cur_dict:
                if cur_dict[tag] > limit:
                    significant_tags[tag] = cur_dict[tag]
            persons_dict[person] = significant_tags

    current_person = Person.objects.filter(slug=person_slug)[0]
    try:
        current_tags = persons_dict[current_person.full_name]
    except:
        current_tags = []

    relations = {}
    coef_values = []
    for person in persons_dict:
        if person != current_person.full_name:
            s1 = set([e for e in current_tags])
            s2 = set([e for e in persons_dict[person]])
            coef = _calculate_relation_coefficient(s1, s2)
            coef_values.append(coef)
            relations[person] = coef

    coef_values = sorted(coef_values)

    sorted_relations = sorted(relations.iteritems(), key=operator.itemgetter(1), reverse=True)[:50]
    sorted_relations = filter(lambda (name, coef): coef > 0.075, sorted_relations)

    if top:
        sorted_relations = sorted_relations[:5]

    return_dict = {
        'related_persons': sorted_relations,
        'length': len(sorted_relations),
        'chart_height': (len(sorted_relations) + 1) * 32,
        'top': top,
        'person_slug': person_slug,
        'person_name': current_person.full_name,
    }

    return render(request, "charts/people/related_persons.html", return_dict)


###     topic_cloud(entity_slug, person_slug)
####################################################################################################

def topic_cloud(request, entity_slug, person_slug=None):

    tags = None
    items = []
    person = None

    if entity_slug == 'publications':
        if person_slug:
            person = Person.objects.get(slug=person_slug)
            publication_ids = person.publications.all().values_list('id', flat=True)
            tags = PublicationTag.objects.filter(publication_id__in=publication_ids)

        else:
            tags = PublicationTag.objects.all()

    elif entity_slug == 'projects':
        if person_slug:
            person = Person.objects.get(slug=person_slug)
            project_ids = person.projects.all().values_list('id', flat=True)
            tags = ProjectTag.objects.filter(project_id__in=project_ids)

        else:
            tags = ProjectTag.objects.all()

    if tags:
        tag_list = tags.values_list('tag__name', flat=True)
        counter = Counter(tag_list)
        ord_dict = OrderedDict(sorted(counter.items(), key=lambda t: t[1]))

        items = ord_dict.items()
        items = items[len(items)-100:]

    return_dict = {
        'tag_dict': dict(items),
        'entity_slug': entity_slug,
        'person': person,
        'entity_slug': entity_slug,
    }

    return render(request, "charts/topics/cloud.html", return_dict)
