# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import Organization
from .forms import OrganizationForm, OrganizationSearchForm

from entities.projects.models import Project, ConsortiumMember
from entities.projects.forms import *

# Create your views here.

PAGINATION_NUMBER = settings.ORGANIZATIONS_PAGINATION


#########################
# View: organization_index
#########################

def organization_index(request):
    organizations = Organization.objects.all().order_by('full_name')

    if request.method == 'POST':
        form = OrganizationSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            orgs = []

            for organization in organizations:
                if query in slugify(organization.name):
                    orgs.append(organization)

            organizations = orgs

    else:
        form = OrganizationSearchForm()

    paginator = Paginator(organizations, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        organizations = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        organizations = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        organizations = paginator.page(paginator.num_pages)

    return render_to_response("organizations/index.html", {
            'organizations': organizations,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: organization_info
#########################

def organization_info(request, slug):
    organization = get_object_or_404(Organization, slug=slug)

    projects_leaded = Project.objects.filter(project_leader=organization.id).order_by('full_name')

    consortium_ids = ConsortiumMember.objects.filter(organization_id=organization.id).values('project_id')
    projects = Project.objects.filter(id__in=consortium_ids).order_by('full_name')

    return render_to_response("organizations/info.html", {
            'organization': organization,
            'projects_leaded': projects_leaded,
            'projects': projects,
        },
        context_instance = RequestContext(request))
