# coding: utf-8

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

from .models import Project, FundingAmount, AssignedPerson, ConsortiumMember, Funding
# from .forms import ProjectForm, ProjectSearchForm, FundingAmountFormSet, AssignedPersonFormSet, ConsortiumMemberFormSet
from .forms import ProjectSearchForm

from entities.persons.models import Person

from entities.organizations.models import Organization

from entities.funding_programs.models import FundingProgram

# Create your views here.

PAGINATION_NUMBER = settings.PROJECTS_PAGINATION


#########################
# View: project_index
#########################

def project_index(request):
    projects = Project.objects.all().order_by('full_name')

    if request.method == 'POST':
        form = ProjectSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            projs = []

            for project in projects:

                if query in slugify(project.full_name):
                    projs.append(project)

            projects = projs

    else:
        form = ProjectSearchForm()

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
        },
        context_instance = RequestContext(request))


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

    persons = AssignedPerson.objects.filter(project_id=project.id)

    consortium_members = ConsortiumMember.objects.filter(project_id=project.id).order_by('organization')

    return render_to_response("projects/info.html", {
            'project': project,
            'persons': persons,
            'fundings': fundings,
            'funding_programs': funding_programs,
            'funding_amounts': funding_amounts,
            'consortium_members': consortium_members,
        },
        context_instance=RequestContext(request))


#########################
# View: email_project
#########################

@login_required
def email_project(request, slug):
    project = get_object_or_404(Project, slug=slug)

    funding_program = FundingProgram.objects.get(id=project.funding_program_id)

    lpms = AssignedPerson.objects.filter(project_id=project.id, role='Project manager').values('employee_id')
    project_managers = Person.objects.filter(id__in=lpms).order_by('name', 'first_surname', 'second_surname')

    lprs = AssignedPerson.objects.filter(project_id=project.id, role='Principal researcher').values('employee_id')
    principal_researchers = Person.objects.filter(id__in=lprs).order_by('name', 'first_surname', 'second_surname')

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
