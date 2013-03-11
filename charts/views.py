# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.db.models import Sum, Min, Max

# from django.contrib.auth.decorators import login_required

from funding_programs.models import FundingProgram

from projects.models import Project, FundingAmount

# Create your views here.


#########################
# View: chart_index
#########################

def chart_index(request):
    return render_to_response("charts/index.html", {
        },
        context_instance = RequestContext(request))


#########################
# View: total_incomes
#########################

def total_incomes(request):
    min_year = FundingAmount.objects.aggregate(Min('year'))
    max_year = FundingAmount.objects.aggregate(Max('year'))

    min_year = min_year.get('year__min')
    max_year = max_year.get('year__max')

    incomes = []

    for year in range(min_year, max_year + 1):
        income = FundingAmount.objects.filter(year = year).aggregate(Sum('amount'))
        incomes.append({'key': year, 'value': income})

    return render_to_response("charts/total_incomes.html", {
                'incomes': incomes,
        },
        context_instance = RequestContext(request))


#########################
# View: incomes_by_year
#########################

def incomes_by_year(request, year):
    europe = 0
    spain = 0
    euskadi = 0

    year_incomes = FundingAmount.objects.filter(year = year)

    for year_income in year_incomes:
        project = Project.objects.get(id = year_income.project_id)
        funding_program = FundingProgram.objects.get(id = project.funding_program_id)

        area = funding_program.geographical_scope

        if area == 'Europe':
            europe += year_income.amount
        if area == 'Spain':
            spain += year_income.amount
        if area == 'Euskadi':
            euskadi += year_income.amount

    return render_to_response("charts/incomes_by_year.html", {
            'europe': europe,
            'spain': spain,
            'euskadi': euskadi,
            'year': year,
        },
        context_instance = RequestContext(request))


#########################
# View: incomes_by_year_and_scope
#########################

def incomes_by_year_and_scope(request, year, scope):
    project_incomes = []

    year_incomes = FundingAmount.objects.filter(year = year)

    for year_income in year_incomes:
        project = Project.objects.get(id = year_income.project_id)
        funding_program = FundingProgram.objects.get(id = project.funding_program_id)

        area = funding_program.geographical_scope

        if area == scope:
            project_incomes.append({'key': project.title, 'value': year_income.amount})

    return render_to_response("charts/incomes_by_year_and_scope.html", {
            'project_incomes': project_incomes,
            'year': year,
            'scope': scope,
        },
        context_instance = RequestContext(request))


#########################
# View: incomes_by_project_index
#########################

def incomes_by_project_index(request):
    projects = Project.objects.all().order_by('title')

    return render_to_response("charts/incomes_by_project_index.html", {
            'projects': projects,
        },
        context_instance = RequestContext(request))


#########################
# View: incomes_by_project
#########################

def incomes_by_project(request, project_slug):
    project_incomes = []

    project = Project.objects.get(slug = project_slug)

    funding_amounts = FundingAmount.objects.filter(project_id = project.id)

    for funding_amount in funding_amounts:
        project_incomes.append({'key': funding_amount.year, 'value': funding_amount.amount})

    return render_to_response("charts/incomes_by_project.html", {
            'project': project,
            'project_incomes': project_incomes,
        },
        context_instance = RequestContext(request))
