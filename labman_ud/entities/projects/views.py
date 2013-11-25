# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from .forms import ProjectSearchForm
from .models import Project, FundingAmount, AssignedPerson, ConsortiumMember, Funding, RelatedPublication, ProjectTag, ProjectType

from entities.funding_programs.models import FundingProgram
from entities.persons.models import Person
from entities.publications.models import Publication
from entities.utils.models import Role, Tag

# Create your views here.


###########################################################################
# View: project_index
###########################################################################

def project_index(request, tag_slug=None, status_slug=None, project_type_slug=None, query_string=None):
    tag = None
    status = None
    project_type = None

    clean_index = False

    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        project_ids = ProjectTag.objects.filter(tag=tag).values('project_id')
        projects = Project.objects.filter(id__in=project_ids)

    if status_slug:
        status = status_slug.replace('-', ' ').capitalize()
        projects = Project.objects.filter(status=status)

    if project_type_slug:
        project_type = ProjectType.objects.get(slug=project_type_slug)
        projects = Project.objects.filter(project_type=project_type.id)

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

    # dictionary to be returned in render_to_response()
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'project_type': project_type,
        'projects': projects,
        'projects_length': projects_length,
        'query_string': query_string,
        'status': status,
        'tag': tag,
    }

    return render_to_response("projects/index.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: project_info
###########################################################################

def project_info(request, slug):

    project = get_object_or_404(Project, slug=slug)

    fundings = Funding.objects.filter(project_id=project.id)

    funding_ids = []
    funding_program_ids = []

    for funding in fundings:
        funding_ids.append(funding.id)
        funding_program_ids.append(funding.funding_program.id)

    funding_programs = FundingProgram.objects.filter(pk__in=funding_program_ids)

    funding_amounts = FundingAmount.objects.filter(funding_id__in=funding_ids).order_by('year')

    related_publications_ids = RelatedPublication.objects.filter(project=project.id).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).order_by('-year')

    principal_researchers = []
    project_managers = []
    researchers = []

    assigned_persons = AssignedPerson.objects.filter(project_id=project.id)

    for assigned_person in assigned_persons:
        role = Role.objects.get(id=assigned_person.role.id)
        person = Person.objects.get(id=assigned_person.person_id)

        try:
            start_month = assigned_person.start_date.strftime('%B')
            start_year = assigned_person.start_date.year
            start_date = u'%s %s' % (start_month, start_year)

        except:
            start_date = None

        try:
            end_month = assigned_person.end_date.strftime('%B')
            end_year = assigned_person.end_date.year
            end_date = u'%s %s' % (end_month, end_year)

        except:
            end_date = None

        working_period = None

        if start_date and end_date:
            working_period = u'(from %s to %s)' % (start_date, end_date)

        if start_date and not end_date:
            working_period = u'(since %s)' % (start_date)

        person_item = {
            'description': assigned_person.description,
            'full_name': person.full_name,
            'is_active': person.is_active,
            'slug': person.slug,
            'working_period': working_period,
        }

        if role.slug == 'principal-researcher':
            principal_researchers.append(person_item)

        if role.slug == 'project-manager':
            project_managers.append(person_item)

        if role.slug == 'researcher':
            researchers.append(person_item)

    consortium_members = ConsortiumMember.objects.filter(project_id=project.id).order_by('organization')

    tag_ids = ProjectTag.objects.filter(project=project.id).values('tag_id')
    tags = Tag.objects.filter(id__in=tag_ids).order_by('name')
    # tags = tags.extra(select={'length': 'Length(name)'}).order_by('length')

    logo = project.logo if project.logo else None

    # dictionary to be returned in render_to_response()
    return_dict = {
        'consortium_members': consortium_members,
        'funding_amounts': funding_amounts,
        'funding_programs': funding_programs,
        'fundings': fundings,
        'logo': logo,
        'principal_researchers': principal_researchers,
        'project': project,
        'project_managers': project_managers,
        'related_publications': related_publications,
        'researchers': researchers,
        'tags': tags,
    }

    return render_to_response("projects/info.html", return_dict, context_instance=RequestContext(request))


###########################################################################
# View: project_tag_cloud
###########################################################################

def project_tag_cloud(request):

    tag_dict = {}

    tags = ProjectTag.objects.all()

    for tag in tags:
        t = tag.tag.name

        if t in tag_dict.keys():
            tag_dict[t] = tag_dict[t] + 1

        else:
            tag_dict[t] = 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'tag_dict': tag_dict,
    }

    return render_to_response('projects/tag_cloud.html', return_dict, context_instance=RequestContext(request))
