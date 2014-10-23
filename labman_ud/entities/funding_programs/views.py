# -*- encoding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify

from django.db.models import Sum, Min, Max

from .models import FundingProgram
from .forms import FundingProgramSearchForm

from entities.projects.models import Project, Funding, FundingAmount

# Create your views here.


###########################################################################
# View: funding_program_index
###########################################################################

def funding_program_index(request):
    funding_programs = FundingProgram.objects.all().order_by('short_name')

    if request.method == 'POST':
        form = FundingProgramSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            fps = []

            for funding_program in funding_programs:
                if (query in slugify(funding_program.full_name)) or (query in slugify(funding_program.short_name)):
                    fps.append(funding_program)

            funding_programs = fps

    else:
        form = FundingProgramSearchForm()

    return_dict = {
        'funding_programs': funding_programs,
        'funding_programs_length': len(funding_programs),
        'form': form,
    }

    return render(request, "funding_programs/index.html", return_dict)


def funding_program_info(request, slug):
    funding_program = get_object_or_404(FundingProgram, slug=slug)

    fundings = Funding.objects.filter(funding_program_id=funding_program.id)

    projects = Project.objects.filter(id__in=fundings.values('project_id'))

    dates = Project.objects.filter(id__in=fundings.values('project_id')).aggregate(min_year=Min('start_year'), max_year=Max('end_year'))

    min_year = dates['min_year']
    max_year = dates['max_year']

    number_of_projects = {}
    incomes = {}

    datum = []
    years = []

    for year in range(min_year, max_year + 1):
        years.append(year)
        number_of_projects[year] = 0
        for project in projects:
            if (project.start_year <= year) and (project.end_year >= year):
                number_of_projects[year] = number_of_projects[year] + 1

        income = FundingAmount.objects.filter(year=year, funding_id__in=fundings.values('id')).aggregate(value=Sum('own_amount'))
        if income['value'] is None:
            income['value'] = 0
        incomes[year] = float(income['value'])

        datum.append([year, number_of_projects[year], incomes[year]])

    projects = Project.objects.filter(id__in=fundings.values('project_id')).order_by('start_year', 'full_name')

    return_dict = {
        'funding_program': funding_program,
        'projects': projects,
        'datum': datum,
        'min_year': min_year,
        'max_year': max_year,
    }

    return render(request, "funding_programs/info.html", return_dict)
