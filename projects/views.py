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

from .models import Project, FundingAmount, AssignedEmployee, ConsortiumMember
from .forms import ProjectForm, ProjectSearchForm, FundingAmountFormSet, AssignedEmployeeFormSet, ConsortiumMemberFormSet

from employees.models import Employee

from organizations.models import Organization

from funding_programs.models import FundingProgram

# Create your views here.

PAGINATION_NUMBER = settings.PROJECTS_PAGINATION


#########################
# View: project_index
#########################

def project_index(request):
    projects = Project.objects.all().order_by('title')

    if request.method == 'POST':
        form = ProjectSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            projs = []

            for project in projects:

                if query in slugify(project.title):
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
# View: add_project
#########################

@login_required
def add_project(request):
    error_badges = []

    project = None

    current_year = None
    end_year = None

    project_form = ProjectForm(prefix='project_form')
    funding_amount_formset = FundingAmountFormSet(instance=Project(), prefix='funding_amount_formset')
    assigned_employee_formset = AssignedEmployeeFormSet(instance=Project(), prefix='assigned_employee_formset')
    consortium_member_formset = ConsortiumMemberFormSet(instance=Project(), prefix='consortium_member_formset')

    if request.POST:
        project_form = ProjectForm(request.POST, prefix='project_form')

        # start project_form validation

        if project_form.is_valid():
            project = project_form.save(commit=False)

            funding_amount_formset = FundingAmountFormSet(request.POST, instance=project, prefix='funding_amount_formset')
            assigned_employee_formset = AssignedEmployeeFormSet(request.POST, instance=project, prefix='assigned_employee_formset')
            consortium_member_formset = ConsortiumMemberFormSet(request.POST, instance=project, prefix='consortium_member_formset')

            cd_p = project_form.cleaned_data

            current_year = cd_p['start_year']
            end_year = cd_p['end_year']

            project.project_type = cd_p['project_type'].encode('utf-8')
            project.title = cd_p['title'].encode('utf-8')
            project.description = cd_p['description'].encode('utf-8')
            project.homepage = cd_p['homepage']
            project.start_month = cd_p['start_month']
            project.start_year = cd_p['start_year']
            project.end_month = cd_p['end_month']
            project.end_year = cd_p['end_year']
            project.status = cd_p['status'].encode('utf-8')
            project.project_code = cd_p['project_code'].encode('utf-8')
            project.total_funds = cd_p['total_funds']
            project.total_funds_deusto = cd_p['total_funds_deusto']
            project.observations = cd_p['observations'].encode('utf-8')

            project.funding_program = cd_p['funding_program']
            project.project_leader = cd_p['project_leader']

            try:
                project.logo = request.FILES['project_form-logo']
            except:
                    pass

            project.save()

            if 'project' in error_badges:
                error_badges.remove('project')

            if 'funding_program' in error_badges:
                error_badges.remove('funding_program')

        else:
            if request.POST.get('project_form_funding_program') is None:
                error_badges.append('funding_program')
            else:
                error_badges.remove('funding_program')
            error_badges.append('project')

        # end project_form validation

        # start funding_amount_formset validation

        if funding_amount_formset.is_valid():
            total_funding = 0
            for funding_amount_form in funding_amount_formset:
                if (len(funding_amount_form.cleaned_data) > 0) and (current_year <= end_year):
                    cd_fa = funding_amount_form.cleaned_data

                    funding_amount = FundingAmount(
                        project=project,
                        amount=cd_fa['amount'],
                        year=current_year,
                    )

                    total_funding += funding_amount.amount

                    funding_amount.save()

                    current_year += 1

                else:
                    print "No fundings amounts to save"

            project.total_funds_deusto = total_funding
            project.save()

        # end funding_amount_formset validation

        # start assigned_employee_formset validation

        if assigned_employee_formset.is_valid():
            for assigned_employee_form in assigned_employee_formset:
                if (len(assigned_employee_form.cleaned_data) > 0):
                    cd_ae = assigned_employee_form.cleaned_data

                    assigned_employee_form.project = project
                    assigned_employee_form.employee = cd_ae['employee']
                    assigned_employee_form.role = cd_ae['role']

                    assigned_employee_form.save()

                else:
                    print "No assigned employees to save"

            assigned_employee_formset.save()

            if 'assigned_employees' in error_badges:
                error_badges.remove('assigned_employees')

        else:
            error_badges.append('assigned_employees')
            try:
                project.delete()
            except:
                pass

        # end assigned_employee_formset validation

        # start consortium_member_formset validation

        if consortium_member_formset.is_valid():
            for consortium_member_form in consortium_member_formset:
                    if (len(consortium_member_form.cleaned_data) > 0):
                        cd_cm = consortium_member_form.cleaned_data

                        consortium_member = ConsortiumMember(
                            project=project,
                            organization=cd_cm['organization'],
                        )

                        consortium_member.save()

                    else:
                        print "No consortium members to save"

            if 'consortium_members' in error_badges:
                error_badges.remove('consortium_members')

        else:
            error_badges.append('consortium_members')
            try:
                project.delete()
            except:
                pass

        # start consortium_member_formset validation

        try:
            return HttpResponseRedirect(reverse('email_project', args = (project.slug,)))
        except:
            pass

    else:
        project_form = ProjectForm(prefix='project_form')
        funding_amount_formset = FundingAmountFormSet(instance=Project(), prefix='funding_amount_formset')
        assigned_employee_formset = AssignedEmployeeFormSet(instance=Project(), prefix='assigned_employee_formset')
        consortium_member_formset = ConsortiumMemberFormSet(instance=Project(), prefix='consortium_member_formset')

    return render_to_response("projects/add.html", {
            'error_badges': error_badges,
            'project_form': project_form,
            'funding_amount_formset': funding_amount_formset,
            'assigned_employee_formset': assigned_employee_formset,
            'consortium_member_formset': consortium_member_formset,
        },
        context_instance = RequestContext(request))


#########################
# View: project_info
#########################

def project_info(request, slug):
    project = get_object_or_404(Project, slug=slug)

    funding_program = FundingProgram.objects.get(id=project.funding_program_id)

    lprs = AssignedEmployee.objects.filter(project_id=project.id, role='Principal researcher').values('employee_id')
    principal_researchers = Employee.objects.filter(id__in=lprs).order_by('name', 'first_surname', 'second_surname')

    lpms = AssignedEmployee.objects.filter(project_id=project.id, role='Project manager').values('employee_id')
    project_managers = Employee.objects.filter(id__in=lpms).order_by('name', 'first_surname', 'second_surname')

    rs = AssignedEmployee.objects.filter(project_id=project.id, role='Researcher').values('employee_id')
    researchers = Employee.objects.filter(id__in=rs).order_by('name', 'first_surname', 'second_surname')

    funding_amounts = FundingAmount.objects.filter(project_id=project.id)

    consortium_members = ConsortiumMember.objects.filter(project_id=project.id)

    return render_to_response("projects/info.html", {
            'project': project,
            'funding_program': funding_program,
            'principal_researchers': principal_researchers,
            'project_managers': project_managers,
            'researchers': researchers,
            'funding_amounts': funding_amounts,
            'consortium_members': consortium_members,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_project
#########################

@login_required
def edit_project(request, slug):
    error_badges = []

    project = get_object_or_404(Project, slug=slug)
    assigned_employees = AssignedEmployee.objects.filter(project_id=project.id)
    consortium_members = ConsortiumMember.objects.filter(project_id=project.id)
    funding_amounts = FundingAmount.objects.filter(project_id=project.id).order_by('year')

    current_year = 3000
    end_year = 2999

    project_form = ProjectForm(prefix='project_form')
    funding_amount_formset = FundingAmountFormSet(instance=Project(), prefix='funding_amount_formset')
    assigned_employee_formset = AssignedEmployeeFormSet(instance=Project(), prefix='assigned_employee_formset')
    consortium_member_formset = ConsortiumMemberFormSet(instance=Project(), prefix='consortium_member_formset')

    if request.POST:
        project_form = ProjectForm(request.POST, prefix='project_form')

        # start project_form validation

        if project_form.is_valid():

            funding_amount_formset = FundingAmountFormSet(request.POST, instance=project, prefix='funding_amount_formset')
            assigned_employee_formset = AssignedEmployeeFormSet(request.POST, instance=project, prefix='assigned_employee_formset')
            consortium_member_formset = ConsortiumMemberFormSet(request.POST, instance=project, prefix='consortium_member_formset')

            cd_p = project_form.cleaned_data

            current_year = cd_p['start_year']
            end_year = cd_p['end_year']

            project.project_type = cd_p['project_type'].encode('utf-8')
            project.title = cd_p['title'].encode('utf-8')
            project.description = cd_p['description'].encode('utf-8')
            project.homepage = cd_p['homepage']
            project.start_month = cd_p['start_month']
            project.start_year = cd_p['start_year']
            project.end_month = cd_p['end_month']
            project.end_year = cd_p['end_year']
            project.status = cd_p['status'].encode('utf-8')
            project.project_code = cd_p['project_code'].encode('utf-8')
            project.total_funds = cd_p['total_funds']
            project.total_funds_deusto = cd_p['total_funds_deusto']
            project.observations = cd_p['observations'].encode('utf-8')

            project.funding_program = cd_p['funding_program']
            project.project_leader = cd_p['project_leader']

            try:
                project.logo = request.FILES['project_form-logo']
            except:
                    pass

            project.save()

            if 'project' in error_badges:
                error_badges.remove('project')

        else:
            error_badges.append('project')

        # end project_form validation

        # start funding_amount_formset validation

        if funding_amount_formset.is_valid():
            total_funding = 0
            for funding_amount_form in funding_amount_formset:
                if (len(funding_amount_form.cleaned_data) > 0) and (current_year <= end_year):
                    cd_fa = funding_amount_form.cleaned_data

                    funding_amount = FundingAmount.objects.get(project_id=project.id, year=current_year)

                    funding_amount.amount = cd_fa['amount']

                    total_funding += cd_fa['amount']

                    funding_amount.save()

                    current_year += 1

                else:
                    print "No fundings amounts to save"

            if 'funding_amount' in error_badges:
                error_badges.remove('funding_amount')

            project.total_funds_deusto = total_funding
            project.save()

        else:
            error_badges.append('funding_amount')

        # end funding_amount_formset validation

        # start assigned_employee_formset validation

        if assigned_employee_formset.is_valid():
            for assigned_employee_form in assigned_employee_formset:
                if (len(assigned_employee_form.cleaned_data) > 0):
                    cd_ae = assigned_employee_form.cleaned_data

                    assigned_employee_form.project = project
                    assigned_employee_form.employee = cd_ae['employee']
                    assigned_employee_form.role = cd_ae['role']

                    assigned_employee_form.save()

                else:
                    print "No assigned employees to save"

            assigned_employee_formset.save()

            if 'assigned_employees' in error_badges:
                error_badges.remove('assigned_employees')

        else:
            error_badges.append('assigned_employees')

        # end assigned_employee_formset validation

        # start consortium_member_formset validation

        if consortium_member_formset.is_valid():
            for consortium_member_form in consortium_member_formset:
                if (len(consortium_member_form.cleaned_data) > 0):
                    cd_cm = consortium_member_form.cleaned_data

                    consortium_member_form.project = project
                    consortium_member_form.organization = cd_cm['organization']

                    consortium_member_form.save()

                else:
                    print "No consortium members to save"

            if 'consortium_members' in error_badges:
                error_badges.remove('consortium_members')

        else:
            error_badges.append('consortium_members')

        # start consortium_member_formset validation

        try:
            return HttpResponseRedirect(reverse('email_project', args=(project.slug,)))
        except:
            pass

    else:
        project_data = {
            'project_type': project.project_type,
            'title': project.title,
            'slug': project.slug,
            'description': project.description,
            'homepage': project.homepage,
            'start_month': project.start_month,
            'start_year': project.start_year,
            'end_month': project.end_month,
            'end_year': project.end_year,
            'status': project.status,
            'project_code': project.project_code,
            'total_funds': project.total_funds,
            'total_funds_deusto': project.total_funds_deusto,
            'observations': project.observations,
            'funding_program': project.funding_program,
            'project_leader': project.project_leader,
        }

        # FORMS

        project_form = ProjectForm(
            prefix='project_form',
            initial=project_data,
        )

        funding_amount_formset = FundingAmountFormSet(
            instance=Project(),
            prefix='funding_amount_formset'
        )

        assigned_employee_formset = AssignedEmployeeFormSet(
            instance=Project(),
            prefix='assigned_employee_formset'
        )

        consortium_member_formset = ConsortiumMemberFormSet(
            instance=Project(),
            prefix='consortium_member_formset'
        )

    return render_to_response("projects/edit.html", {
            'project': project,
            'project_form': project_form,
            'funding_amounts': funding_amounts,
            'funding_amount_formset': funding_amount_formset,
            'assigned_employees': assigned_employees,
            'assigned_employee_formset': assigned_employee_formset,
            'consortium_members': consortium_members,
            'consortium_member_formset': consortium_member_formset,
        },
        context_instance = RequestContext(request))


#########################
# View: email_project
#########################

@login_required
def email_project(request, slug):
    project = get_object_or_404(Project, slug=slug)

    funding_program = FundingProgram.objects.get(id=project.funding_program_id)

    lpms = AssignedEmployee.objects.filter(project_id=project.id, role='Project manager').values('employee_id')
    project_managers = Employee.objects.filter(id__in=lpms).order_by('name', 'first_surname', 'second_surname')

    lprs = AssignedEmployee.objects.filter(project_id=project.id, role='Principal researcher').values('employee_id')
    principal_researchers = Employee.objects.filter(id__in=lprs).order_by('name', 'first_surname', 'second_surname')

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
# View: delete_project
#########################

@login_required
def delete_project(request, slug):
    project = get_object_or_404(Project, slug=slug)
    project.delete()

    return HttpResponseRedirect(reverse('project_index'))


#########################
# View: delete_employee_from_project
#########################

@login_required
def delete_employee_from_project(request, employee_slug, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    employee = get_object_or_404(Employee, slug=employee_slug)

    assigned_employee = get_object_or_404(AssignedEmployee, project_id=project.id, employee_id=employee.id)
    assigned_employee.delete()

    return HttpResponseRedirect(reverse('edit_project', args=(project.slug,)))


#########################
# View: delete_employee_from_project
#########################

@login_required
def delete_organization_from_project(request, organization_slug, project_slug):
    project = get_object_or_404(Project, slug=project_slug)
    organization = get_object_or_404(Organization, slug=organization_slug)

    consortium_member = get_object_or_404(ConsortiumMember, project_id=project.id, organization_id=organization.id)
    consortium_member.delete()

    return HttpResponseRedirect(reverse('edit_project', args=(project.slug,)))
