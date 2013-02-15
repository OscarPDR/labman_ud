# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from organizations.models import Organization
from organizations.forms import OrganizationForm

from projects.models import Project
from projects.forms import *

# Create your views here.

PAGINATION_NUMBER = 5


#########################
# View: organization_index
#########################

def organization_index(request):
    organizations = Organization.objects.all().order_by('name')
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
        },
        context_instance = RequestContext(request))


#########################
# View: add_organization
#########################

@login_required
def add_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            organization = Organization(
                name = cd['name'].encode('utf-8'),
                country = cd['country'].encode('utf-8'),
                homepage = cd['homepage'].encode('utf-8'),
            )

            try:
                organization.logo = request.FILES['logo']
            except:
                pass

            organization.save()

            return HttpResponseRedirect(reverse('organization_index'))
    else:
        form = OrganizationForm()

    return render_to_response("organizations/add.html", {
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: organization_info
#########################

def organization_info(request, slug):
    organization = get_object_or_404(Organization, slug = slug)

    projects_leaded = Project.objects.filter(project_leader = organization.id).order_by('title')

    consortium_ids = ConsortiumMember.objects.filter(organization_id = organization.id).values('project_id')
    projects = Project.objects.filter(id__in = consortium_ids).order_by('title')

    return render_to_response("organizations/info.html", {
            'organization': organization,
            'projects_leaded': projects_leaded,
            'projects': projects,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_organization
#########################

@login_required
def edit_organization(request, slug):
    organization = get_object_or_404(Organization, slug = slug)

    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():

            cd = form.cleaned_data

            organization.name = cd['name'].encode('utf-8')
            organization.country = cd['country'].encode('utf-8')
            organization.homepage = cd['homepage'].encode('utf-8')

            try:
                organization.logo = request.FILES['logo']
            except:
                pass

            organization.save()

            return HttpResponseRedirect(reverse('organization_index'))
    else:
        data = {
            'name': organization.name,
            'country': organization.country,
            'homepage': organization.homepage,
            'logo': organization.logo,
        }

        form = OrganizationForm(initial = data)

    return render_to_response("organizations/edit.html", {
            'organization': organization,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: delete_organization
#########################

@login_required
def delete_organization(request, slug):
    organization = get_object_or_404(Organization, slug = slug)
    organization.delete()

    return HttpResponseRedirect(reverse('organization_index'))
