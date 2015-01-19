# coding: utf-

import threading
import weakref
from inflection import titleize

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.syndication.views import Feed

from .forms import ProjectSearchForm
from .models import *
from .utils import *

from entities.funding_programs.models import FundingProgram, FundingProgramLogo
from entities.persons.models import Person
from entities.publications.models import Publication
from entities.utils.models import Role, Tag

from collections import OrderedDict, Counter


###########################################################################
# View: project_index
###########################################################################

def project_index(request, tag_slug=None, status_slug=None, project_type_slug=None, query_string=None):
    tag = None
    status = None
    project_type = None

    clean_index = False

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
        form = ProjectSearchForm(request.POST)
        if form.is_valid():
            query_string = form.cleaned_data['text']

            return HttpResponseRedirect(reverse('view_project_query', kwargs={'query_string': query_string}))

    else:
        form = ProjectSearchForm()

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

    if (projects_length > 0):
        last_created = Project.objects.order_by('-log_created')[0]
        last_modified = Project.objects.order_by('-log_modified')[0]

    else:
        last_created = None
        last_modified = None

    project_types = Project.objects.all().values_list('project_type', flat=True)

    counter = Counter(project_types)
    ord_dict = OrderedDict(sorted(counter.items(), key=lambda t: t[1]))

    items = ord_dict.items()

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Projects',
        'clean_index': clean_index,
        'form': form,
        'last_created': last_created,
        'last_modified': last_modified,
        'project_type': project_type,
        'project_type_info': dict(items),
        'projects': projects,
        'projects_length': projects_length,
        'query_string': query_string,
        'status': status,
        'tag': tag,
    }

    return render(request, "projects/index.html", return_dict)


###########################################################################
# View: project_info
###########################################################################

def project_info(request, project_slug):
    project = get_object_or_404(Project, slug=project_slug)

    # dictionary to be returned in render(request, )
    return_dict = __build_project_information(project)
    return_dict['web_title'] = project.full_name

    if project.project_type == 'Internal project':
        return render(request, "projects/info_internal_project.html", return_dict)

    elif project.project_type == 'External project':
        return render(request, "projects/info_external_project.html", return_dict)

    else:
        return render(request, "projects/info.html", return_dict)


###########################################################################
# View: project_funding_details
###########################################################################

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


###########################################################################
# View: project_assigned_persons
###########################################################################

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


###########################################################################
# View: project_consortium_members
###########################################################################

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


###########################################################################
# View: project_related_publications
###########################################################################

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


###########################################################################
# View: project_tag_cloud
###########################################################################

def project_tag_cloud(request):
    tags = ProjectTag.objects.all().values_list('tag__name', flat=True)

    counter = Counter(tags)
    ord_dict = OrderedDict(sorted(counter.items(), key=lambda t: t[1]))

    items = ord_dict.items()
    items = items[len(items)-100:]

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Projects tag cloud',
        'tag_dict': dict(items),
    }

    return render(request, 'projects/tag_cloud.html', return_dict)


############################################################################
# Function: __build_project_information
############################################################################

def __build_project_information(project):
    tag_ids = ProjectTag.objects.filter(project=project.id).values('tag_id')
    tags = Tag.objects.filter(id__in=tag_ids).order_by('name')

    related_publications_ids = RelatedPublication.objects.filter(project=project.id).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).order_by('-year')

    internal_project = project.project_type == 'Internal project'
    external_project = project.project_type == 'External project'

    # dictionary to be returned in render(request, )
    return {
        'is_internal': internal_project,
        'is_external': external_project,
        'logo': project.logo if project.logo else None,
        'project': project,
        'related_publications': related_publications,
        'tags': tags,
    }


###########################################################################
# Feed: projects feeds
###########################################################################

class LatestProjectsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestProjectsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    title = "MORElab projects"
    description = "MORElab projects"

    def get_object(self, request):
        self.__request.request = weakref.proxy(request)
        return super(LatestProjectsFeed, self).get_object(request)

    def link(self, obj):
        url = reverse('project_index')
        return self.__request.request.build_absolute_uri(url)

    def items(self):
        return Project.objects.order_by('-log_created')[:30]

    def item_title(self, item):
        return item.full_name

    def item_description(self, item):
        return item.description

    def item_link(self, item):
        url = reverse('project_info', args=[item.slug or 'no-slug-found'])
        return self.__request.request.build_absolute_uri(url)
