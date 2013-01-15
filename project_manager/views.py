# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

from project_manager.models import *
from project_manager.forms import *


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

    if request.method == 'POST':
        project_form = ProjectForm(request.POST, request.FILES, prefix = 'project_form')
        if project_form.is_valid():
            project = project_form.save(commit = False)

            print "Commit = False"

            funding_program_form = FundingProgramForm(request.POST, instance = project, prefix = 'funding_program_form')
            funding_amount_formset = FundingAmountFormSet(request.POST, instance = project, prefix = 'funding_amount_formset')

            cd_p = project_form.cleaned_data

            project_type = cd_p['project_type']
            title = cd_p['title']
            description = cd_p['description']
            homepage = cd_p['homepage']
            start_year = cd_p['start_year']
            end_year = cd_p['end_year']
            status = cd_p['status']
            currency = cd_p['currency']
            observations = cd_p['observations']

            project = Project(
                project_type = project_type.encode('utf-8'),
                title = title.encode('utf-8'),
                description = description.encode('utf-8'),
                homepage = homepage,
                start_year = start_year,
                end_year = end_year,
                status = status.encode('utf-8'),
                currency = currency.encode('utf-8'),
                observations = observations.encode('utf-8'),
            )

            # if request.FILES['logo']:
            #     project.logo = request.FILES['logo']

            project.save()

            print "project.save()"

            if funding_program_form.is_valid():
                cd_f = funding_program_form.cleaned_data

                name = cd_f['name']
                project_code = cd_f['project_code']
                start_month = cd_f['start_month']
                start_year = cd_f['start_year']
                end_month = cd_f['end_month']
                end_year = cd_f['end_year']
                concession_year = cd_f['concession_year']
                geographical_scope = cd_f['geographical_scope']

                funding_program = FundingProgram(
                    name = name.encode('utf-8'),
                    project_code = project_code.encode('utf-8'),
                    start_month = start_month,
                    start_year = start_year,
                    end_month = end_month,
                    end_year = end_year,
                    concession_year = concession_year,
                    geographical_scope = geographical_scope.encode('utf-8'),
                )

                funding_program.project = project

                funding_program.save()

                print "funding_program.save()"

            for i in range(start_year, end_year + 1):
                if funding_amount_formset.is_valid():
                    for funding_amount_form in funding_amount_formset:
                        if (i <= end_year) and (len(funding_amount_form.cleaned_data) > 0):
                            cd_fa = funding_amount_form.cleaned_data

                            funding_amount_form.amount = cd_fa['amount']
                            funding_amount_form.year = i

                            funding_amount_form.save()

                        else:
                            print "No fundings amounts to save"

                    funding_amount_formset.save()

            return HttpResponseRedirect("/correct")
    else:
        project_form = ProjectForm(prefix = 'project_form')
        funding_program_form = FundingProgramForm(instance = Project(), prefix = 'funding_program_form')
        funding_amount_formset = FundingAmountFormSet(instance = Project(), prefix = 'funding_amount_formset')

    return render_to_response("project_manager/add.html", {
            "project_form": project_form,
            "funding_program_form": funding_program_form,
            "funding_amount_formset": funding_amount_formset,
        },
        context_instance=RequestContext(request))


def delete_project(request, slug):
    project = get_object_or_404(Project, slug = slug)
    project.delete()

    return redirect('project_index')
