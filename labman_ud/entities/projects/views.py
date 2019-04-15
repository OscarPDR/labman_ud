# coding: utf-

import threading
import weakref
import json
import re
from inflection import titleize

from django.core import serializers
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.syndication.views import Feed
from django.db.models import Q, Sum

from .forms import ProjectSearchForm
from .models import *
from .utils import *

from entities.funding_programs.models import FundingProgram, FundingProgramLogo
from entities.persons.models import Person
from entities.publications.models import Publication
from entities.utils.models import Role, Tag
from entities.news.models import ProjectRelatedToNews
from entities.datasets.models import DatasetProject, Dataset

from labman_setup.models import *
from labman_ud.util import *

from collections import OrderedDict, Counter


###		project_index
####################################################################################################

def project_index(request, tag_slug=None, status_slug=None, project_type_slug=None, query_string=None):
    tag = None
    status = None
    start_date = None
    start_range = None
    end_date = None
    end_range = None
    project_type = None
    form_project_types = None
    form_project_status = None
    form_tags = None
    form_funds_range = None
    form_from_total_funds = None
    form_to_total_funds = None
    form_participants_name = {}
    form_participants_role = {}
    clean_index = False

    request.session['max_year'] = MAX_YEAR_LIMIT
    request.session['min_year'] = MIN_YEAR_LIMIT

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        project_ids = ProjectTag.objects.filter(tag=tag).values('project_id')
        projects = Project.objects.filter(id__in=project_ids)

    if status_slug:
        status = status_slug.replace('-', ' ').capitalize()
        projects = Project.objects.filter(status=status)

    if project_type_slug:
        project_type = titleize(project_type_slug).capitalize()
        projects = Project.objects.filter(project_type=project_type)

    if not tag_slug and not status_slug and not project_type_slug:
        clean_index = True
        projects = Project.objects.all()

    projects = projects.order_by('-start_year', '-end_year', 'full_name')

    if request.method == 'POST':
        form_member_field_count = request.POST.get('member_field_count')
        form = ProjectSearchForm(request.POST, extra=form_member_field_count)

        if form.is_valid():
            query_string = form.cleaned_data['text']
            start_date = form.cleaned_data['start_date']
            start_range = form.cleaned_data['start_range']
            end_date = form.cleaned_data['end_date']
            end_range = form.cleaned_data['end_range']
            form_project_types = form.cleaned_data['project_types']
            form_project_status = form.cleaned_data['status']
            form_from_total_funds = form.cleaned_data['from_total_funds']
            form_to_total_funds = form.cleaned_data['to_total_funds']
            form_funds_range = form.cleaned_data['funds_range']
            form_tags = form.cleaned_data['tags']

            for my_tuple in form.fields.items():
                if my_tuple[0].startswith('participant_name_'):
                    form_names = form.cleaned_data[my_tuple[0]]
                    if form_names:
                        form_participants_name[my_tuple[0][-1:]] = form_names
                elif my_tuple[0].startswith('participant_role_'):
                    form_roles = form.cleaned_data[my_tuple[0]]
                    if form_roles:
                        form_participants_role[my_tuple[0][-1:]] = list(form_roles.values())

            # tratamiento con los filter, y devolver "projects" filtrado
            # return a 'index' con los projectos filtrados

            if start_date:
                month_year = start_date.split('/')
                if start_range == '<=':
                    projects = projects.filter(Q(start_year__lt=month_year[1]) |
                     (Q(start_year=month_year[1]) & Q(start_month__lte=month_year[0])))
                elif start_range == '<':
                    projects = projects.filter(Q(start_year__lt=month_year[1]) |
                        (Q(start_year=month_year[1]) & Q(start_month__lt=month_year[0])))
                elif start_range == '>=':
                    projects = projects.filter(Q(start_year__gt=month_year[1]) |
                     (Q(start_year=month_year[1]) & Q(start_month__gte=month_year[0])))
                elif start_range == '>':
                    projects = projects.filter(Q(start_year__gt=month_year[1]) |
                     (Q(start_year=month_year[1]) & Q(start_month__gt=month_year[0])))
                elif start_range == '==':
                    projects = projects.filter(Q(start_year=month_year[1]) & Q(start_month=month_year[0]))

            if end_date:
                month_year = end_date.split('/')
                if end_range == '<=':
                    projects = projects.filter(Q(end_year__lt=month_year[1]) |
                     (Q(end_year=month_year[1]) & Q(end_month__lte=month_year[0])))
                elif end_range == '<':
                    projects = projects.filter(Q(end_year__lt=month_year[1]) |
                     (Q(end_year=month_year[1]) & Q(end_month__lt=month_year[0])))
                elif end_range == '>=':
                    projects = projects.filter(Q(end_year__gt=month_year[1]) |
                     (Q(end_year=month_year[1]) & Q(end_month__gte=month_year[0])))
                elif end_range == '>':
                    projects = projects.filter(Q(end_year__gt=month_year[1]) |
                     (Q(end_year=month_year[1]) & Q(end_month__gt=month_year[0])))
                elif end_range == '==':
                    projects = projects.filter(Q(end_year=month_year[1]) & Q(end_month=month_year[0]))

            if form_project_types:
                projects = projects.filter(project_type__in=form_project_types)

            if form_project_status:
                projects = projects.filter(status__in=form_project_status)

            if form_tags:
                projects = projects.filter(projecttag__tag__name__in=form_tags)

            if form_from_total_funds:
                if form_funds_range == '==':
                    funding_sum = FundingAmount.objects.all().values('funding_id').annotate(Sum('own_amount'))
                    filtered_funding_ids = funding_sum.filter(own_amount__sum=form_from_total_funds).values_list('funding_id', flat=True)
                    projects = projects.filter(funding__id__in=filtered_funding_ids)
                elif form_funds_range == '<':
                    funding_sum = FundingAmount.objects.all().values('funding_id').annotate(Sum('own_amount'))
                    filtered_funding_ids = funding_sum.filter(own_amount__sum__lt=form_from_total_funds).values_list('funding_id', flat=True)
                    projects = projects.filter(funding__id__in=filtered_funding_ids)
                elif form_funds_range == '<=':
                    funding_sum = FundingAmount.objects.all().values('funding_id').annotate(Sum('own_amount'))
                    filtered_funding_ids = funding_sum.filter(own_amount__sum__lte=form_from_total_funds).values_list('funding_id', flat=True)
                    projects = projects.filter(funding__id__in=filtered_funding_ids)
                elif form_funds_range == '>':
                    funding_sum = FundingAmount.objects.all().values('funding_id').annotate(Sum('own_amount'))
                    filtered_funding_ids = funding_sum.filter(own_amount__sum__gt=form_from_total_funds).values_list('funding_id', flat=True)
                    projects = projects.filter(funding__id__in=filtered_funding_ids)
                elif form_funds_range == '>=':
                    funding_sum = FundingAmount.objects.all().values('funding_id').annotate(Sum('own_amount'))
                    filtered_funding_ids = funding_sum.filter(own_amount__sum__gte=form_from_total_funds).values_list('funding_id', flat=True)
                    projects = projects.filter(funding__id__in=filtered_funding_ids)
                elif form_funds_range == '-':
                    funding_sum = FundingAmount.objects.all().values('funding_id').annotate(Sum('own_amount'))
                    filtered_funding_ids = funding_sum.filter(own_amount__sum__gte=form_from_total_funds)
                    if form_to_total_funds:
                        filtered_funding_ids = filtered_funding_ids.filter(own_amount__sum__lte=form_to_total_funds)
                    filtered_funding_ids = filtered_funding_ids.values_list('funding_id', flat=True)
                    projects = projects.filter(funding__id__in=filtered_funding_ids)

            found = True

            if form_participants_name:
                group_projects = []
                for key, name in form_participants_name.iteritems():
                    person_id = Person.objects.filter(slug__contains=slugify(name)).values_list('id', flat=True)
                    if person_id and found:
                        person_projects_set = set()
                        for _id in person_id:
                            participant_roles_ids = []
                            if key in form_participants_role:
                                for role in form_participants_role[key]:
                                    participant_roles_ids.append(role['id'])
                            if participant_roles_ids:
                                person_projects = AssignedPerson.objects.all().filter(Q(person_id=_id) & Q(role__in=participant_roles_ids)).values_list('project_id', flat=True)
                                if person_projects:
                                    person_projects_set.update(person_projects)
                            else:
                                person_projects = AssignedPerson.objects.all().filter(person_id=_id).values_list('project_id', flat=True)
                                if person_projects:
                                    person_projects_set.update(person_projects)
                        group_projects.append(person_projects_set)
                    else:
                        found = False
                if group_projects and found:
                    projects = projects.filter(id__in=list(set.intersection(*group_projects)))

            query = slugify(query_string)
            projs = []

            person_ids = Person.objects.filter(slug__contains=query).values('id')
            project_ids = AssignedPerson.objects.filter(person_id__in=person_ids).values('project_id')
            project_ids = set([x['project_id'] for x in project_ids])

            for project in projects:
                if (query in slugify(project.full_name)) or (project.id in project_ids):
                    projs.append(project)

            projects = projs

            if not found:
                projects = []

            session_filter_dict = {
                'form_start_date': start_date,
                'form_start_range': start_range,
                'form_end_date': end_date,
                'form_end_range': end_range,
                'form_project_types': form_project_types,
                'form_project_status': form_project_status,
                'form_tags': form_tags,
                'projects': serializers.serialize('json', projects),
                'form_funds_range': form_funds_range,
                'form_from_total_funds': str(form_from_total_funds),
                'form_to_total_funds': str(form_to_total_funds),
                'form_participants_name': form_participants_name,
                'form_participants_role': json.dumps(form_participants_role),
                'form_member_field_count': len(form_participants_name),
                'query_string': query_string,
            }

            request.session['filtered'] = session_filter_dict

            return HttpResponseRedirect(reverse('filtered_project_query'))

    else:
        if 'filtered' in request.session.keys():
            p = re.compile(ur'projects\/filtered(\/\?page=[1-9]+)?')

            if  re.search(p, request.path) == None:
                del request.session['filtered']
                form = ProjectSearchForm(extra=1)
            else:
                member_field_count = request.session['filtered']['form_member_field_count']
                if member_field_count == 0:
                    member_field_count = 1
                form = ProjectSearchForm(extra=member_field_count)
                start_date = request.session['filtered']['form_start_date']
                start_range = request.session['filtered']['form_start_range']
                end_date = request.session['filtered']['form_end_date']
                end_range = request.session['filtered']['form_end_range']
                form_project_types = request.session['filtered']['form_project_types']
                form_project_status = request.session['filtered']['form_project_status']
                form_tags = request.session['filtered']['form_tags']
                form_tags = request.session['filtered']['form_tags']
                projects = []
                for deserialized_object in serializers.deserialize('json', request.session['filtered']['projects']):
                    projects.append(deserialized_object.object)
                form_funds_range = request.session['filtered']['form_funds_range']
                form_from_total_funds = request.session['filtered']['form_from_total_funds']
                form_to_total_funds = request.session['filtered']['form_to_total_funds']
                form_participants_name = request.session['filtered']['form_participants_name']
                form_participants_role = json.loads(request.session['filtered']['form_participants_role'])
                query_string = request.session['filtered']['query_string']
                clean_index = False
        else:
            form = ProjectSearchForm(extra=1)

    if query_string:
        query = slugify(query_string)
        projs = []

        person_ids = Person.objects.filter(slug__contains=query).values('id')
        project_ids = AssignedPerson.objects.filter(person_id__in=person_ids).values('project_id')
        project_ids = set([x['project_id'] for x in project_ids])

        for project in projects:
            if (query in slugify(project.full_name)) or (project.id in project_ids):
                projs.append(project)

        projects = projs
        clean_index = False

    projects_length = len(projects)

    project_model_list = ['Project']

    last_entry = get_last_model_update_log_entry('projects', project_model_list)

    project_types = Project.objects.all().values_list('project_type', flat=True)

    counter = Counter(project_types)
    ord_dict = OrderedDict(sorted(counter.items(), key=lambda t: t[1]))

    items = ord_dict.items()

    status_info = Project.objects.all().values_list('status', flat=True)
    status_items = OrderedDict(sorted(Counter(status_info).items(), key=lambda t: t[1])).items()

    tags_id_info = Project.objects.all().values_list('tags', flat=True)
    tags_info = Tag.objects.filter(id__in=tags_id_info).order_by('name').values_list('name', flat=True)

    roles_id = AssignedPerson.objects.all().distinct().values_list('role', flat=True)
    roles = Role.objects.filter(id__in=roles_id).order_by('name')

    # Retrieves all the full names of authors.
    participants_info = AssignedPerson.objects.all() \
        .distinct('person__full_name').order_by() \
        .values_list('person__full_name', flat=True)

    # dictionary to be returned in render(request, )
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'last_entry': last_entry,
        'project_type': project_type,
        'project_type_info': dict(items),
        'project_status_info' : dict(status_items),
        'project_tags_info' : tags_info,
        'projects': projects,
        'projects_length': projects_length,
        'query_string': query_string,
        'status': status,
        'tag': tag,
        'roles' : roles,
        'form_start_date' : start_date,
        'form_start_range' : start_range,
        'form_end_date' : end_date,
        'form_end_range' : end_range,
        'form_project_types' : form_project_types,
        'form_project_status' : form_project_status,
        'form_tags': form_tags,
        'form_funds_range' : form_funds_range,
        'form_from_total_funds' : form_from_total_funds,
        'form_to_total_funds' : form_to_total_funds,
        'form_participants_name' : form_participants_name,
        'form_participants_role' : form_participants_role,
        'participants_info' : participants_info,
        'web_title': u'Projects',
    }

    return render(request, "projects/index.html", return_dict)


###		project_info
####################################################################################################

def project_info(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    # dictionary to be returned in render(request, )
    return_dict = __build_project_information(project)
    return_dict['web_title'] = project.full_name

    return render(request, "projects/info.html", return_dict)


###		project_funding_details
####################################################################################################

def project_funding_details(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    fundings = Funding.objects.filter(project_id=project.id)

    funding_ids = []
    funding_program_ids = []

    for funding in fundings:
        funding_ids.append(funding.id)
        funding_program_ids.append(funding.funding_program.id)

    funding_programs = FundingProgram.objects.filter(pk__in=funding_program_ids)

    funding_amounts = FundingAmount.objects.filter(funding_id__in=funding_ids).order_by('year')

    total_funds = None

    if funding_amounts:
        total_funds = 0

        for funding in funding_amounts:
            total_funds += funding.own_amount

    funding_program_logos = FundingProgramLogo.objects.filter(funding_program__in=funding_program_ids)

    # dictionary to be returned in render(request, )
    return_dict = __build_project_information(project)
    return_dict.update({
        'web_title': u'%s - Funding details' % project.full_name,
        'funding_amounts': funding_amounts,
        'funding_program_logos': funding_program_logos,
        'funding_programs': funding_programs,
        'fundings': fundings,
        'total_funds': total_funds,
    })

    return render(request, "projects/funding_details.html", return_dict)


###		project_assigned_persons
####################################################################################################

def project_assigned_persons(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    people_by_role = OrderedDict()
    people_timeline_by_role = []
    role_colors = []

    assigned_persons = AssignedPerson.objects.filter(project_id=project.id)
    assigned_persons = assigned_persons.order_by(
        'role__relevance_order',
        'start_date',
        'end_date',
        'person__slug',
    )

    for assigned_person in assigned_persons:
        role_name = assigned_person.role.name
        person = assigned_person.person
        description = assigned_person.description

        people_by_role[role_name] = people_by_role.get(role_name, [])
        people_by_role[role_name].append({
            'full_name': person.full_name,
            'slug': person.slug,
            'id': person.id,
            'gender': person.gender,
            'profile_picture_url': person.profile_picture,
            'description': description,
        })

        if not assigned_person.role.exclude_from_charts:
            people_timeline_by_role.append({
                'role': assigned_person.role.name,
                'full_name': person.full_name,
                'start_date': get_person_start_date(assigned_person),
                'end_date': get_person_end_date(assigned_person),
            })

            rgb_color = assigned_person.role.rgb_color

            if rgb_color and rgb_color not in role_colors:
                role_colors.append(str(rgb_color))

    role_colors = list(role_colors) if len(role_colors) > 0 else None

    # dictionary to be returned in render(request, )
    return_dict = __build_project_information(project)
    return_dict.update({
        'chart_height': (len(people_timeline_by_role) + 1) * 45,
        'people_by_role': people_by_role,
        'people_timeline_by_role': people_timeline_by_role,
        'project': project,
        'role_colors': role_colors,
        'roles': Role.objects.all(),
        'web_title': u'%s - Assigned persons' % project.full_name,
    })

    return render(request, "projects/assigned_persons.html", return_dict)


###		project_consortium_members
####################################################################################################

def project_consortium_members(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    consortium_members = ConsortiumMember.objects.filter(project_id=project.id).order_by('organization')

    # dictionary to be returned in render(request, )
    return_dict = __build_project_information(project)
    return_dict.update({
        'web_title': u'%s - Consortium members' % project.full_name,
        'consortium_members': consortium_members,
    })

    return render(request, "projects/consortium_members.html", return_dict)


###     project_related_publications
####################################################################################################

def project_related_publications(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    related_publications_ids = RelatedPublication.objects.filter(project=project.id).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).order_by('-year')

    # dictionary to be returned in render(request, )
    return_dict = __build_project_information(project)
    return_dict.update({
        'web_title': u'%s - Related publications' % project.full_name,
        'related_publications': related_publications,
    })

    return render(request, "projects/related_publications.html", return_dict)


###     project_related_datasets
####################################################################################################

def project_related_datasets(request, project_slug):
    """
    Obtain the related datasets used in this project

    :param request: Type of the request
    :param project_slug: project slug to make the search in DB
    :return:
    """
    project = get_object_or_404(Project, slug=project_slug)

    # Extracting datasets information
    dataset_ids = DatasetProject.objects.filter(project=project.id).values_list('dataset_id', flat=True)
    datasets = Dataset.objects.filter(id__in=dataset_ids)

    # dictionary to be returned in render(request, )
    return_dict = __build_project_information(project)
    return_dict.update({
        'web_title': u'%s - Related datasets' % project.full_name,
        'related_datasets': datasets,
    })

    return render(request, "projects/related_datasets.html", return_dict)


###     project_related_news(project_slug)
####################################################################################################

def project_related_news(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    return_dict = __build_project_information(project)

    return_dict.update({
        'web_title': u'%s - Related news' % project.full_name,
    })

    return render(request, "projects/related_news.html", return_dict)


############################################################################
# Function: __build_project_information
############################################################################

def __build_project_information(project):
    tag_ids = ProjectTag.objects.filter(project=project.id).values('tag_id')
    tags = Tag.objects.filter(id__in=tag_ids).order_by('name')

    # Obtaining related publications
    related_publications_ids = RelatedPublication.objects.filter(project=project.id).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).order_by('-year')

    # Obtaining related datasets
    related_datasets_ids = DatasetProject.objects.filter(project=project.id).values_list('dataset_id', flat=True)
    related_datasets = Dataset.objects.filter(id__in=related_datasets_ids)

    related_news = ProjectRelatedToNews.objects.filter(project=project).order_by('-news__created')

    # dictionary to be returned in render(request, )
    return {
        'is_internal': project.project_type in ['Internal project', 'External project'],
        'logo': project.logo if project.logo else None,
        'project': project,
        'related_publications': related_publications,
        'related_datasets': related_datasets,
        'related_news': related_news,
        'tags': tags,
    }


####################################################################################################
# Feed: projects feeds
####################################################################################################

class LatestProjectsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestProjectsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    try:
        _settings = LabmanDeployGeneralSettings.objects.get()
        research_group_short_name = _settings.research_group_short_name

    except:
        research_group_short_name = u'Our'

    title = u'%s projects' % research_group_short_name
    description = u'%s projects' % research_group_short_name

    def get_object(self, request):
        self.__request.request = weakref.proxy(request)
        return super(LatestProjectsFeed, self).get_object(request)

    def link(self, obj):
        url = reverse('project_index')
        return self.__request.request.build_absolute_uri(url)

    def items(self):
        return Project.objects.order_by('-id')[:30]

    def item_title(self, item):
        return item.full_name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        url = reverse('project_info', args=[item.slug or 'no-slug-found'])
        return self.__request.request.build_absolute_uri(url)
