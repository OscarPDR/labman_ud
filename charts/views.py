# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.conf import settings

from django.db.models import Sum, Min, Max

from entities.funding_programs.models import FundingProgram

from entities.projects.models import Project, FundingAmount, Funding

from entities.utils.models import GeographicalScope


BASE_TEMPLATE = 'labman_ud/base.html'
CLEAN_BASE_TEMPLATE = 'labman_ud/clean_base.html'


# Create your views here.


#########################
# View: chart_index
#########################

def chart_index(request):
    return render_to_response("charts/index.html", {}, context_instance=RequestContext(request))


#########################
# View: total_incomes
#########################

def total_incomes(request):
    base_template = CLEAN_BASE_TEMPLATE if request.META['HTTP_HOST'] == settings.HOST_URL else BASE_TEMPLATE
    path = str(request.path).replace('total_', '')

    min_year = FundingAmount.objects.aggregate(Min('year'))
    max_year = FundingAmount.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    incomes = []

    for year in range(min_year, max_year + 1):
        income = FundingAmount.objects.filter(year=year).aggregate(value=Sum('own_amount'))
        if income['value'] is None:
            income['value'] = 0
        incomes.append({'key': year, 'value': income['value']})

    return render_to_response("charts/total_incomes.html", {
            'incomes': incomes,
            'base_template': base_template,
            'path': path,
        },
        context_instance=RequestContext(request))


#########################
# View: incomes_by_year
#########################

def incomes_by_year(request, year):
    base_template = CLEAN_BASE_TEMPLATE if request.META['HTTP_HOST'] == settings.HOST_URL else BASE_TEMPLATE
    path = str(request.path).replace('total_', '') + '/'

    incomes = {}

    geographical_scopes = GeographicalScope.objects.all()

    for geographical_scope in geographical_scopes:
        incomes[geographical_scope.name] = 0

    year_incomes = FundingAmount.objects.filter(year=year)

    for year_income in year_incomes:
        funding = Funding.objects.get(id=year_income.funding_id)
        funding_program = FundingProgram.objects.get(id=funding.funding_program.id)
        scope = funding_program.geographical_scope.name
        incomes[scope] = incomes[scope] + year_income.own_amount

    return render_to_response("charts/incomes_by_year.html", {
            'incomes': incomes,
            'year': year,
            'base_template': base_template,
            'path': path,
        },
        context_instance=RequestContext(request))


#########################
# View: incomes_by_year_and_scope
#########################

def incomes_by_year_and_scope(request, year, scope):
    base_template = CLEAN_BASE_TEMPLATE if request.META['HTTP_HOST'] == settings.HOST_URL else BASE_TEMPLATE

    project_incomes = []

    year_incomes = FundingAmount.objects.filter(year=year)

    for year_income in year_incomes:
        funding = Funding.objects.get(id=year_income.funding_id)
        funding_program = FundingProgram.objects.get(id=funding.funding_program_id)
        project = Project.objects.get(id=funding.project_id)

        if funding_program.geographical_scope.name == scope:
            project_incomes.append({'key': project.full_name, 'value': year_income.own_amount})

    return render_to_response("charts/incomes_by_year_and_scope.html", {
            'project_incomes': project_incomes,
            'year': year,
            'scope': scope,
            'base_template': base_template,
        },
        context_instance=RequestContext(request))


#########################
# View: incomes_by_project_index
#########################

def incomes_by_project_index(request):
    projects = Project.objects.all().order_by('slug')

    return render_to_response("charts/incomes_by_project_index.html", {
            'projects': projects,
        },
        context_instance=RequestContext(request))


#########################
# View: incomes_by_project
#########################

def incomes_by_project(request, project_slug):
    project = Project.objects.get(slug=project_slug)

    funding_ids = Funding.objects.filter(project_id=project.id).values('id')

    project_incomes = FundingAmount.objects.filter(funding_id__in=funding_ids).values('year').annotate(total=Sum('own_amount'))

    return render_to_response("charts/incomes_by_project.html", {
            'project': project,
            'project_incomes': project_incomes,
        },
        context_instance=RequestContext(request))


#########################
# View: total_incomes_by_scope
#########################

def total_incomes_by_scope(request):
    base_template = CLEAN_BASE_TEMPLATE if request.META['HTTP_HOST'] == settings.HOST_URL else BASE_TEMPLATE

    incomes = {}

    geographical_scopes = GeographicalScope.objects.all()

    for geographical_scope in geographical_scopes:
        incomes[geographical_scope.name] = 0

    funding_amounts = FundingAmount.objects.all()

    min_year = FundingAmount.objects.aggregate(Min('year'))
    max_year = FundingAmount.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    incomes = {}

    for year in range(min_year, max_year + 1):
        incomes[year] = {}
        for scope in geographical_scopes:
            incomes[year][scope.name] = 0

    for funding_amount in funding_amounts:
        funding = Funding.objects.get(id=funding_amount.funding_id)
        funding_program = FundingProgram.objects.get(id=funding.funding_program.id)
        scope = funding_program.geographical_scope.name
        incomes[funding_amount.year][scope] = incomes[funding_amount.year][scope] + funding_amount.own_amount

    total_incomes = []

    for year in range(min_year, max_year + 1):
        euskadi = float(incomes[year]['Euskadi'])
        spain = float(incomes[year]['Spain'])
        europe = float(incomes[year]['Europe'])
        total_incomes.append([year, euskadi, spain, europe, (euskadi+spain+europe)])

    return render_to_response("charts/total_incomes_by_scope.html", {
            'incomes': incomes,
            'total_incomes': total_incomes,
            'year': year,
            'base_template': base_template,
        },
        context_instance=RequestContext(request))
