# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import FundingProgram
from .forms import FundingProgramForm, FundingProgramSearchForm

from entities.projects.models import Project, Funding

# Create your views here.

PAGINATION_NUMBER = settings.FUNDING_PROGRAMS_PAGINATION


#########################
# View: funding_program_index
#########################

def funding_program_index(request):
    funding_programs = FundingProgram.objects.all().order_by('full_name')

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

    paginator = Paginator(funding_programs, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        funding_programs = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        funding_programs = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        funding_programs = paginator.page(paginator.num_pages)
    return render_to_response("funding_programs/index.html", {
            'funding_programs': funding_programs,
            'form': form,
        },
        context_instance = RequestContext(request))


def funding_program_info(request, slug):
    funding_program = get_object_or_404(FundingProgram, slug=slug)

    project_ids = Funding.objects.filter(funding_program_id=funding_program.id).values('project_id')

    projects = Project.objects.filter(id__in=project_ids).order_by('start_year', 'full_name')

    return render_to_response("funding_programs/info.html", {
            'funding_program': funding_program,
            'projects': projects,
        },
        context_instance = RequestContext(request))
