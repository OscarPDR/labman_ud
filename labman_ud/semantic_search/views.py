# -*- encoding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.db.models import Sum, Min, Max

from semantic_search.forms import SemanticSearchForm

from entities.funding_programs.models import FundingProgram

from entities.projects.models import Project, AssignedPerson, Funding

from entities.utils.models import GeographicalScope


# Create your views here.


###########################################################################
# View: semantic_search
###########################################################################

def semantic_search(request):
    active = False
    title = ''
    researchers = None
    status = 'Any'
    scope = None
    start_year = 2004
    end_year = 2013
    and_or = 'OR'
    projects = None
    if request.method == 'POST':
        form = SemanticSearchForm(request.POST)
        if form.is_valid():
            active = True

            cd = form.cleaned_data

            title = cd['title']
            researchers = cd['researchers']
            status = cd['status']
            scope = cd['scope']
            start_year = int(cd['start_year'])
            end_year = int(cd['end_year'])
            and_or = cd['and_or']

            probable_projects = Project.objects.all()

            if title != '':
                probable_projects = probable_projects.filter(full_name__icontains=title)

            if status != 'Any':
                probable_projects = probable_projects.filter(status=status)

            if scope:
                geographical_scope = GeographicalScope.objects.get(name=scope)
                funding_program_ids = FundingProgram.objects.filter(geographical_scope=geographical_scope.id).values('id')
                project_ids = Funding.objects.filter(funding_program__in=funding_program_ids).values('project_id')
                probable_projects = probable_projects.filter(id__in=project_ids)

            probable_projects = probable_projects.filter(start_year__gte=start_year)
            probable_projects = probable_projects.filter(end_year__lte=end_year)

            probable_projects = probable_projects.order_by('slug')

            # TODO: Researchers filter

            if researchers == []:
                projects = probable_projects

            else:
                projects = []

                researcher_ids = []
                for researcher in researchers:
                    researcher_ids.append(researcher.id)

                for project in probable_projects:
                    assigned_employees = AssignedPerson.objects.filter(project_id=project.id)
                    employees_ids = []
                    for employee in assigned_employees:
                        employees_ids.append(employee.employee_id)

                    if set(researcher_ids).issubset(employees_ids) and and_or == 'AND':
                        projects.append(project)

                    if (len(set(researcher_ids) & set(employees_ids)) > 0) and and_or == 'OR':
                        projects.append(project)

    else:
        form = SemanticSearchForm()

    return render_to_response("semantic_search/searcher.html", {
            'active': active,
            'form': form,
            'title': title,
            'researchers': researchers,
            'status': status,
            'scope': scope,
            'start_year': start_year,
            'end_year': end_year,
            'and_or': and_or,
            'projects': projects,
        },
        context_instance=RequestContext(request))
