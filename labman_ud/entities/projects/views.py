# coding: utf-8

import datetime
from datetime import date

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.contrib.auth.decorators import login_required

from django.conf import settings

from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Project, FundingAmount, AssignedPerson, ConsortiumMember, Funding, RelatedPublication, ProjectTag, ProjectType, ProjectLogo
from .forms import ProjectSearchForm

from entities.persons.models import Person

from entities.organizations.models import Organization

from entities.funding_programs.models import FundingProgram

from entities.publications.models import Publication

from entities.utils.models import Role, Tag

# Create your views here.

PAGINATION_NUMBER = settings.PROJECTS_PAGINATION


#########################
# View: project_index
#########################

def project_index(request, tag_slug=None, status_slug=None, project_type_slug=None):
    tag = None
    status = None
    project_type = None

    query_string = None

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
            query = slugify(query_string)

            projs = []

            person_ids = Person.objects.filter(slug__contains=query).values('id')
            project_ids = AssignedPerson.objects.filter(person_id__in=person_ids).values('project_id')
            project_ids = set([x['project_id'] for x in project_ids])

            print project_ids

            for project in projects:
                if (query in slugify(project.full_name)) or (project.id in project_ids):
                    projs.append(project)
                    
            projects = projs
            clean_index = False

    else:
        form = ProjectSearchForm()

    projects_length = len(projects)

    paginator = Paginator(projects, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        projects = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        projects = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        projects = paginator.page(paginator.num_pages)

    return render_to_response("projects/index.html", {
            "projects": projects,
            'form': form,
            'projects_length': projects_length,
            'tag': tag,
            'status': status,
            'project_type': project_type,
            'query_string': query_string,
            'clean_index': clean_index,
        },
        context_instance=RequestContext(request))


#########################
# View: project_info
#########################

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
                'full_name': person.full_name,
                'is_active': person.is_active,
                'slug': person.slug,
                'working_period': working_period,
                'description': assigned_person.description,
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

    try:
        project_logo = ProjectLogo.objects.get(project=project.id)
        logo = project_logo.logo
    except:
        logo = None

    return render_to_response("projects/info.html", {
            'project': project,
            'project_managers': project_managers,
            'principal_researchers': principal_researchers,
            'researchers': researchers,
            'fundings': fundings,
            'funding_programs': funding_programs,
            'funding_amounts': funding_amounts,
            'consortium_members': consortium_members,
            'related_publications': related_publications,
            'tags': tags,
            'logo': logo,
        },
        context_instance=RequestContext(request))


#########################
# View: email_project
#########################

@login_required
def email_project(request, slug):
    project = get_object_or_404(Project, slug=slug)

    funding_program = FundingProgram.objects.get(id=project.funding_program_id)

    project_manager = Role.objects.get(name='Project Manager')

    lpms = AssignedPerson.objects.filter(project_id=project.id, role=project_manager.id).values('employee_id')
    project_managers = Person.objects.filter(id__in=lpms).order_by('full_name')

    principal_researcher = Role.objects.get(name='Principal Researcher')

    lprs = AssignedPerson.objects.filter(project_id=project.id, role=principal_researcher.id).values('employee_id')
    principal_researchers = Person.objects.filter(id__in=lprs).order_by('full_name')

    lrs = AssignedPerson.objects.filter(project_id=project.id, role=researcher.id).values('employee_id')
    researcher = Role.objects.get(name='Researcher')

    persons = Person.objects.filter(id__in=lrs).order_by('full_name')

    project_leader = Organization.objects.get(id=project.project_leader_id)

    consortium_members = []

    for consortium_member in ConsortiumMember.objects.all().filter(project_id=project.id):
        org = Organization.objects.get(id=consortium_member.organization.id)
        consortium_members.append(org.name)

    html_content = render_to_string('projects/project_email_template.html', {
        'project': project,
        'funding_program': funding_program,
        'project_managers': project_managers,
        'principal_researchers': principal_researchers,
        'project_leader': project_leader,
        'consortium_members': consortium_members,
    })
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        '[NEW PROJECT]: ' + project.title,                # subject
        text_content,                                             # message
        settings.PROJECTS_SENDER_EMAIL,              # from
        settings.PROJECTS_RECEPTOR_EMAILS,       # to
    )

    try:
        image_file = open(project.logo.path, 'rb')
        msg_image = MIMEImage(image_file.read())
        image_file.close()

        msg_image.add_header('Content-ID', '<image>', filename=project.logo.path)
        msg.attach(msg_image)
    except:
        pass

    try:
        image_file = open(funding_program.logo.path, 'rb')
        msg_image = MIMEImage(image_file.read())
        image_file.close()

        msg_image.add_header('Content-ID', '<image>', filename = funding_program.logo.path)
        msg.attach(msg_image)
    except:
        pass

    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponseRedirect(reverse('project_index'))


#########################
# View: project_tag_cloud
#########################

def project_tag_cloud(request):

    tag_dict = {}

    tags = ProjectTag.objects.all()

    for tag in tags:
        t = tag.tag.name
        if t in tag_dict.keys():
            tag_dict[t] = tag_dict[t] + 1
        else:
            tag_dict[t] = 1

    return render_to_response('projects/tag_cloud.html', {
            'tag_dict': tag_dict,
        },
        context_instance=RequestContext(request))
