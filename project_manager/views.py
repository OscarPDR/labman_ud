# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


from django.db.models import Sum
from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from project_manager.models import *
from project_manager.forms import *

from employee_manager.models import *
from employee_manager.forms import *

from organization_manager.models import *
from organization_manager.forms import *

# Create your views here.

PAGINATION_NUMBER = 5


#########################
# View: project_index
#########################

def project_index(request):
    projects = Project.objects.all().order_by('title')
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

    return render_to_response("project_manager/index.html", {
            "projects": projects,
        },
        context_instance = RequestContext(request))


#########################
# View: add_project
#########################

def add_project(request):
    project_form = ProjectForm(prefix = 'project_form')
    funding_program_form = FundingProgramForm(instance = Project(), prefix = 'funding_program_form')
    funding_amount_formset = FundingAmountFormSet(instance = Project(), prefix = 'funding_amount_formset')
    assigned_employee_formset = AssignedEmployeeFormSet(instance = Project(), prefix = 'assigned_employee_formset')
    consortium_member_formset = ConsortiumMemberFormSet(instance = Project(), prefix = 'consortium_member_formset')
    project_leader_form = ProjectLeaderForm(instance = Project(), prefix = 'project_leader_form')

    if request.POST:
        project_form = ProjectForm(request.POST, prefix = 'project_form')
        if project_form.is_valid():
            project = project_form.save(commit = False)

            funding_program_form = FundingProgramForm(request.POST, instance = project, prefix = 'funding_program_form')
            funding_amount_formset = FundingAmountFormSet(request.POST, instance = project, prefix = 'funding_amount_formset')
            assigned_employee_formset = AssignedEmployeeFormSet(request.POST, instance = project, prefix = 'assigned_employee_formset')
            consortium_member_formset = ConsortiumMemberFormSet(request.POST, instance = project, prefix = 'consortium_member_formset')
            project_leader_form = ProjectLeaderForm(request.POST, instance = project, prefix = 'project_leader_form')

            cd_p = project_form.cleaned_data

            project.project_type = cd_p['project_type'].encode('utf-8')
            project.title = cd_p['title'].encode('utf-8')
            project.description = cd_p['description'].encode('utf-8')
            project.homepage = cd_p['homepage']
            project.start_year = cd_p['start_year']
            project.end_year = cd_p['end_year']
            project.status = cd_p['status'].encode('utf-8')
            project.observations = cd_p['observations'].encode('utf-8')

            try:
                project.logo = request.FILES['project_form-logo']
            except:
                    pass

            project.save()

            if funding_program_form.is_valid():
                cd_f = funding_program_form.cleaned_data

                funding_program = FundingProgram(
                    project = project,
                    organization = cd_f['organization'],
                    name = cd_f['name'].encode('utf-8'),
                    project_code = cd_f['project_code'].encode('utf-8'),
                    start_month = cd_f['start_month'],
                    start_year = cd_f['start_year'],
                    end_month = cd_f['end_month'],
                    end_year = cd_f['end_year'],
                    concession_year = cd_f['concession_year'],
                    geographical_scope = cd_f['geographical_scope'].encode('utf-8'),
                )

                try:
                    funding_program.logo = request.FILES['funding_program_form-logo']
                except:
                    pass

                funding_program.save()

                current_year = cd_f['start_year']

            else:
                project.delete()
                print '1'

            if funding_amount_formset.is_valid():
                for funding_amount_form in funding_amount_formset:
                    if (len(funding_amount_form.cleaned_data) > 0) and (current_year <= cd_f['end_year']):
                        cd_fa = funding_amount_form.cleaned_data

                        funding_amount = FundingAmount(
                            project = project,
                            amount = cd_fa['amount'],
                            year = current_year,
                        )

                        funding_amount.save()

                        current_year += 1

                    else:
                        print "No fundings amounts to save"
            else:
                project.delete()
                print '2'

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
            else:
                project.delete()
                print '3'

            if consortium_member_formset.is_valid():
                for consortium_member_form in consortium_member_formset:
                        if (len(consortium_member_form.cleaned_data) > 0):
                            cd_cm = consortium_member_form.cleaned_data

                            consortium_member = ConsortiumMember(
                                project = project,
                                organization = cd_cm['organization'],
                            )

                            consortium_member.save()

                        else:
                            print "No consortium members to save"
            else:
                project.delete()
                print '4'

            if project_leader_form.is_valid():
                if (len(project_leader_form.cleaned_data) > 0):
                    cd_pl = project_leader_form.cleaned_data

                    project_leader = ProjectLeader(
                        project = project,
                        organization = cd_pl['organization']
                    )

                    project_leader.save()
                else:
                    print "No project leader to save"

            return HttpResponseRedirect("/projects/email/" + project.slug)
    else:
        project_form = ProjectForm(prefix = 'project_form')
        funding_program_form = FundingProgramForm(instance = Project(), prefix = 'funding_program_form')
        funding_amount_formset = FundingAmountFormSet(instance = Project(), prefix = 'funding_amount_formset')
        assigned_employee_formset = AssignedEmployeeFormSet(instance = Project(), prefix = 'assigned_employee_formset')
        consortium_member_formset = ConsortiumMemberFormSet(instance = Project(), prefix = 'consortium_member_formset')
        project_leader_form = ProjectLeaderForm(instance = Project(), prefix = 'project_leader_form')

    return render_to_response("project_manager/add.html", {
            "project_form": project_form,
            "funding_program_form": funding_program_form,
            "funding_amount_formset": funding_amount_formset,
            "assigned_employee_formset": assigned_employee_formset,
            "consortium_member_formset": consortium_member_formset,
            "project_leader_form": project_leader_form,
        },
        context_instance = RequestContext(request))


#########################
# View: info_project
#########################

def info_project(request, slug):
    project = get_object_or_404(Project, slug = slug)

    funding_program = FundingProgram.objects.get(project_id = project.id)

    lprs = AssignedEmployee.objects.filter(project_id = project.id, role = 'Principal researcher').values('employee_id')
    principal_researchers = Employee.objects.filter(id__in = lprs).order_by('name', 'first_surname', 'second_surname')

    lpms = AssignedEmployee.objects.filter(project_id = project.id, role = 'Project manager').values('employee_id')
    project_managers = Employee.objects.filter(id__in = lpms).order_by('name', 'first_surname', 'second_surname')

    rs = AssignedEmployee.objects.filter(project_id = project.id, role = 'Researcher').values('employee_id')
    researchers = Employee.objects.filter(id__in = rs).order_by('name', 'first_surname', 'second_surname')

    total_deusto = FundingAmount.objects.filter(project_id = project.id).aggregate(Sum('amount'))

    funding_amounts = FundingAmount.objects.filter(project_id = project.id)

    consortium_members = ConsortiumMember.objects.filter(project_id = project.id)

    project_leader = ProjectLeader.objects.get(project_id = project.id)

    return render_to_response("project_manager/info.html", {
            'project': project,
            'funding_program': funding_program,
            'principal_researchers': principal_researchers,
            'project_managers': project_managers,
            'researchers': researchers,
            'total_deusto': total_deusto,
            'funding_amounts': funding_amounts,
            'project_leader': project_leader,
            'consortium_members': consortium_members,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_project
#########################

def edit_project(request, slug):
    project = get_object_or_404(Project, slug = slug)
    funding_program = get_object_or_404(FundingProgram, project_id = project.id)
    project_leader = get_object_or_404(ProjectLeader, project_id = project.id)
    assigned_employees = AssignedEmployee.objects.filter(project_id = project.id)
    consortium_members = ConsortiumMember.objects.filter(project_id = project.id)

    current_year = 3000
    end_year = 2999

    project_form = ProjectForm(prefix = 'project_form')
    funding_program_form = FundingProgramForm(instance = Project(), prefix = 'funding_program_form')
    funding_amount_formset = FundingAmountFormSet(instance = Project(), prefix = 'funding_amount_formset')
    assigned_employee_formset = AssignedEmployeeFormSet(instance = Project(), prefix = 'assigned_employee_formset')
    consortium_member_formset = ConsortiumMemberFormSet(instance = Project(), prefix = 'consortium_member_formset')
    project_leader_form = ProjectLeaderForm(instance = Project(), prefix = 'project_leader_form')

    if request.POST:
        project_form = ProjectForm(request.POST, prefix = 'project_form')
        if project_form.is_valid():
            # project = project_form.save(commit = False)

            funding_program_form = FundingProgramForm(request.POST, instance = project, prefix = 'funding_program_form')
            funding_amount_formset = FundingAmountFormSet(request.POST, instance = project, prefix = 'funding_amount_formset')
            assigned_employee_formset = AssignedEmployeeFormSet(request.POST, instance = project, prefix = 'assigned_employee_formset')
            consortium_member_formset = ConsortiumMemberFormSet(request.POST, instance = project, prefix = 'consortium_member_formset')
            project_leader_form = ProjectLeaderForm(request.POST, instance = project, prefix = 'project_leader_form')

            cd_p = project_form.cleaned_data

            project.project_type = cd_p['project_type'].encode('utf-8')
            project.title = cd_p['title'].encode('utf-8')
            project.description = cd_p['description'].encode('utf-8')
            project.homepage = cd_p['homepage']
            project.start_year = cd_p['start_year']
            project.end_year = cd_p['end_year']
            project.status = cd_p['status'].encode('utf-8')
            project.observations = cd_p['observations'].encode('utf-8')

            try:
                project.logo = request.FILES['project_form-logo']
            except:
                    pass

            project.save()

            if funding_program_form.is_valid():
                cd_f = funding_program_form.cleaned_data

                funding_program.project = project
                funding_program.organization = cd_f['organization']
                funding_program.name = cd_f['name'].encode('utf-8')
                funding_program.project_code = cd_f['project_code'].encode('utf-8')
                funding_program.start_month = cd_f['start_month']
                funding_program.start_year = cd_f['start_year']
                funding_program.end_month = cd_f['end_month']
                funding_program.end_year = cd_f['end_year']
                funding_program.concession_year = cd_f['concession_year']
                funding_program.geographical_scope = cd_f['geographical_scope'].encode('utf-8')

                try:
                    funding_program.logo = request.FILES['funding_program_form-logo']
                except:
                    pass

                funding_program.save()

                current_year = cd_f['start_year']
                end_year = cd_f['end_year']

            else:
                project.delete()
                print '1'

            if funding_amount_formset.is_valid():
                for funding_amount_form in funding_amount_formset:
                    if (len(funding_amount_form.cleaned_data) > 0) and (current_year <= end_year):
                        cd_fa = funding_amount_form.cleaned_data

                        funding_amount_form.project = project
                        funding_amount_form.amount = cd_fa['amount']
                        funding_amount_form.year = current_year

                        funding_amount.save()

                        current_year += 1

                    else:
                        print "No fundings amounts to save"
            else:
                project.delete()
                print '2'

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
            else:
                project.delete()
                print '3'

            if consortium_member_formset.is_valid():
                for consortium_member_form in consortium_member_formset:
                        if (len(consortium_member_form.cleaned_data) > 0):
                            cd_cm = consortium_member_form.cleaned_data

                            consortium_member_form.project = project
                            consortium_member_form.organization = cd_cm['organization']

                            consortium_member.save()

                        else:
                            print "No consortium members to save"
            else:
                project.delete()
                print '4'

            if project_leader_form.is_valid():
                if (len(project_leader_form.cleaned_data) > 0):
                    cd_pl = project_leader_form.cleaned_data

                    project_leader.project = project
                    project_leader.organization = cd_pl['organization']

                    project_leader.save()

                else:
                    print "No project leader to save"

            return HttpResponseRedirect("/projects/email/" + project.slug)

    else:
        project_data = {
            'project_type': project.project_type,
            'title': project.title,
            'slug': project.slug,
            'description': project.description,
            'homepage': project.homepage,
            'start_year': project.start_year,
            'end_year': project.end_year,
            'status': project.status,
            'total_funds': project.total_funds,
            'observations': project.observations,
        }

        funding_program_data = {
            'organization': funding_program.organization,
            'name': funding_program.name,
            'project_code': funding_program.project_code,
            'start_month': funding_program.start_month,
            'start_year': funding_program.start_year,
            'end_month': funding_program.end_month,
            'end_year': funding_program.end_year,
            'concession_year': funding_program.concession_year,
            'geographical_scope': funding_program.geographical_scope,
        }

        project_leader_data = {
            'organization': project_leader.organization,
        }

        # FORMS

        project_form = ProjectForm(
            prefix = 'project_form',
            initial = project_data,
        )

        funding_program_form = FundingProgramForm(
            instance = Project(),
            prefix = 'funding_program_form',
            initial = funding_program_data,
        )

        funding_amount_formset = FundingAmountFormSet(
            instance = Project(),
            prefix = 'funding_amount_formset'
        )

        assigned_employee_formset = AssignedEmployeeFormSet(
            instance = Project(),
            prefix = 'assigned_employee_formset'
        )

        project_leader_form = ProjectLeaderForm(
            instance = Project(),
            prefix = 'project_leader_form',
            initial = project_leader_data,
        )

        consortium_member_formset = ConsortiumMemberFormSet(instance = Project(), prefix = 'consortium_member_formset')

    print consortium_members

    return render_to_response("project_manager/edit.html", {
            'project': project,
            "project_form": project_form,
            'funding_program_data': funding_program_data,
            "funding_program_form": funding_program_form,
            "funding_amount_formset": funding_amount_formset,
            'assigned_employees': assigned_employees,
            "assigned_employee_formset": assigned_employee_formset,
            'project_leader': project_leader,
            "project_leader_form": project_leader_form,
            'consortium_members': consortium_members,
            "consortium_member_formset": consortium_member_formset,
        },
        context_instance = RequestContext(request))


#########################
# View: email_project
#########################

def email_project(request, slug):
    project = get_object_or_404(Project, slug = slug)

    funding_program = FundingProgram.objects.get(project_id = project.id)

    lpms = AssignedEmployee.objects.filter(project_id = project.id, role = 'Project manager').values('employee_id')
    project_managers = Employee.objects.filter(id__in = lpms).order_by('name', 'first_surname', 'second_surname')

    lprs = AssignedEmployee.objects.filter(project_id = project.id, role = 'Principal researcher').values('employee_id')
    principal_researchers = Employee.objects.filter(id__in = lprs).order_by('name', 'first_surname', 'second_surname')

    print principal_researchers

    total_deusto = FundingAmount.objects.filter(project_id = project.id).aggregate(Sum('amount'))

    project_leader = ProjectLeader.objects.get(project_id = project.id)

    consortium_members = []

    for consortium_member in ConsortiumMember.objects.all().filter(project_id = project.id):
        org = Organization.objects.get(id = consortium_member.organization.id)
        consortium_members.append(org.name)

    html_content = render_to_string('project_manager/project_email_template.html', {
        'project': project,
        'funding_program': funding_program,
        'project_managers': project_managers,
        'principal_researchers': principal_researchers,
        'total_deusto': total_deusto,
        'project_leader': project_leader,
        'consortium_members': consortium_members,
    })
    text_content = strip_tags(html_content)

    msg = EmailMultiAlternatives(
        '[NEW PROJECT]: ' + project.title,        # subject
        text_content,                                     # message
        'oscar.pdr@gmail.com',                      # from
        ['oscar.pdr@gmail.com']                    # to
    )

    try:
        image_file = open(project.logo.path, 'rb')
        msg_image = MIMEImage(image_file.read())
        image_file.close()

        msg_image.add_header('Content-ID', '<image>', filename = project.logo.path)
        msg.attach(msg_image)
    except:
        pass

    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponseRedirect('/projects')


#########################
# View: delete_project
#########################

def delete_project(request, slug):
    project = get_object_or_404(Project, slug = slug)
    project.delete()

    return redirect('project_index')


#########################
# View: delete_employee_from_project
#########################

def delete_employee_from_project(request, employee_slug, project_slug):
    project = get_object_or_404(Project, slug = project_slug)
    employee = get_object_or_404(Employee, slug = employee_slug)

    assigned_employee = get_object_or_404(AssignedEmployee, project_id = project.id, employee_id = employee.id)
    assigned_employee.delete()

    return redirect('/projects/edit/' + project.slug)


#########################
# View: delete_employee_from_project
#########################

def delete_organization_from_project(request, organization_slug, project_slug):
    project = get_object_or_404(Project, slug = project_slug)
    organization = get_object_or_404(Organization, slug = organization_slug)

    consortium_member = get_object_or_404(ConsortiumMember, project_id = project.id, organization_id = organization.id)
    consortium_member.delete()

    return redirect('/projects/edit/' + project.slug)
