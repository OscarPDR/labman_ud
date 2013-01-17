# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

from project_manager.models import *
from project_manager.forms import *

from employee_manager.models import *
from employee_manager.forms import *

from organization_manager.models import *
from organization_manager.forms import *

def project_index(request):
    projects = Project.objects.all()

    return render_to_response("project_manager/index.html", {
            "projects": projects,
        },
        context_instance=RequestContext(request))


def add_project(request):
    project_form = ProjectForm(prefix = 'project_form')
    funding_program_form = FundingProgramForm(instance = Project(), prefix = 'funding_program_form')
    funding_amount_formset = FundingAmountFormSet(instance = Project(), prefix = 'funding_amount_formset')
    assigned_employee_formset = AssignedEmployeeFormSet(instance = Project(), prefix = 'assigned_employee_formset')
    consortium_member_formset = ConsortiumMemberFormSet(instance = Project(), prefix = 'consortium_member_formset')

    if request.POST:
        project_form = ProjectForm(request.POST, prefix = 'project_form')
        if project_form.is_valid():
            project = project_form.save(commit = False)

            funding_program_form = FundingProgramForm(request.POST, instance = project, prefix = 'funding_program_form')
            funding_amount_formset = FundingAmountFormSet(request.POST, instance = project, prefix = 'funding_amount_formset')
            assigned_employee_formset = AssignedEmployeeFormSet(request.POST, instance = project, prefix = 'assigned_employee_formset')
            consortium_member_formset = ConsortiumMemberFormSet(request.POST, instance = project, prefix = 'consortium_member_formset')

            cd_p = project_form.cleaned_data

            project.project_type = cd_p['project_type'].encode('utf-8')
            project.title = cd_p['title'].encode('utf-8')
            project.description = cd_p['description'].encode('utf-8')
            project.homepage = cd_p['homepage']
            project.start_year = cd_p['start_year']
            project.end_year = cd_p['end_year']
            project.status = cd_p['status'].encode('utf-8')
            project.currency = cd_p['currency'].encode('utf-8')
            project.observations = cd_p['observations'].encode('utf-8')

            # if request.FILES['logo']:
            #     project.logo = request.FILES['logo']

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

                funding_program.save()

                current_year = cd_f['start_year']


            # # FIXME
            if funding_amount_formset.is_valid():
                for funding_amount_form in funding_amount_formset:
                    print "funding amount de " + str(current_year)
                    print "hay cleaned data: " + str(len(funding_amount_form.cleaned_data))
                    print str(current_year) + " < " + str(cd_f['end_year'])
                    if (len(funding_amount_form.cleaned_data) > 0) and (current_year <= cd_f['end_year']):
                        print "entra"
                        cd_fa = funding_amount_form.cleaned_data

                        funding_amount = FundingAmount(
                            project = project,
                            amount = cd_fa['amount'],
                            year = current_year,
                        )

                        funding_amount.save()
                        print "funding_amount.save()"

                        current_year += 1

                    else:
                        print "No fundings amounts to save"

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
                            print "No assigned employees to save"

            return HttpResponseRedirect("/proyectos")
    else:
        project_form = ProjectForm(prefix = 'project_form')
        funding_program_form = FundingProgramForm(instance = Project(), prefix = 'funding_program_form')
        funding_amount_formset = FundingAmountFormSet(instance = Project(), prefix = 'funding_amount_formset')
        assigned_employee_formset = AssignedEmployeeFormSet(instance = Project(), prefix = 'assigned_employee_formset')
        consortium_member_formset = ConsortiumMemberFormSet(instance = Project(), prefix = 'consortium_member_formset')

    return render_to_response("project_manager/add.html", {
            "project_form": project_form,
            "funding_program_form": funding_program_form,
            "funding_amount_formset": funding_amount_formset,
            "assigned_employee_formset": assigned_employee_formset,
            "consortium_member_formset": consortium_member_formset,
        },
        context_instance=RequestContext(request))


def delete_project(request, slug):
    project = get_object_or_404(Project, slug = slug)
    project.delete()

    return redirect('project_index')
