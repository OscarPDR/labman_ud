# -*- encoding: utf-8 -*-

from inflection import titleize

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify

from .forms import OrganizationSearchForm
from .models import Organization

from entities.projects.models import Project, ConsortiumMember


# Create your views here.


###########################################################################
# View: organization_index
###########################################################################

def organization_index(request, organization_type_slug=None, query_string=None):
    organization_type = None

    clean_index = False

    if organization_type_slug:
        organization_type = titleize(organization_type_slug).capitalize()
        organizations = Organization.objects.filter(organization_type=organization_type)

    else:
        clean_index = True
        organizations = Organization.objects.all()

    organizations = organizations.order_by('full_name')

    if request.method == 'POST':
        form = OrganizationSearchForm(request.POST)

        if form.is_valid():
            query_string = form.cleaned_data['text']

            return HttpResponseRedirect(reverse('view_organization_query', kwargs={'query_string': query_string}))

    else:
        form = OrganizationSearchForm()

    if query_string:
        query = slugify(query_string)

        orgs = []

        for organization in organizations:
            if query in slugify(organization.full_name):
                orgs.append(organization)

        organizations = orgs
        clean_index = False

    organizations_length = len(organizations)

    # dictionary to be returned in render(request, )
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'organization_type': organization_type,
        'organizations': organizations,
        'organizations_length': organizations_length,
        'query_string': query_string,
    }

    return render(request, "organizations/index.html", return_dict)


###########################################################################
# View: organization_info
###########################################################################

def organization_info(request, slug):
    organization = get_object_or_404(Organization, slug=slug)

    logo = organization.logo if organization.logo else None

    projects_leaded = Project.objects.filter(project_leader=organization.id).order_by('-start_year', '-end_year', 'full_name')

    consortium_ids = ConsortiumMember.objects.filter(organization_id=organization.id).values('project_id')
    projects = Project.objects.filter(id__in=consortium_ids).order_by('-start_year', '-end_year', 'full_name')

    return_dict = {
        'logo': logo,
        'organization': organization,
        'projects': projects,
        'projects_leaded': projects_leaded,
    }

    return render(request, "organizations/info.html", return_dict)
