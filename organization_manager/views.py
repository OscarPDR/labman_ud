# coding: utf-8

# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect

from organization_manager.models import *
from organization_manager.forms import *

def index(request):
    organizations = Organization.objects.all()

    return render_to_response("organization_manager/index.html", {
            "organizations": organizations,
        },
        context_instance = RequestContext(request))

def add_organization(request):
    if request.method == 'POST':
        form = OrganizationForm(request.POST, request.FILES)
        if form.is_valid():

            cd = form.cleaned_data

            name = cd['name']
            country = cd['country']
            homepage = cd['homepage']

            org = Organization(
                name = name.encode('utf-8'), 
                country = country.encode('utf-8'), 
                homepage = homepage.encode('utf-8'),
                logo = request.FILES['logo']
            )

            org.save()

            return HttpResponseRedirect("/organizaciones")
    else:
        form = OrganizationForm()

    return render_to_response("organization_manager/add.html", {
            "form": form,
        },
        context_instance = RequestContext(request))

def edit_organization(request, slug):
    organization = get_object_or_404(Organization, slug = slug)

    if request.method == 'POST':
        form = OrganizationForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data

            organization.name = cd['name'].encode('utf-8')
            organization.country = cd['country'].encode('utf-8')
            organization.homepage = cd['homepage'].encode('utf-8')
            organization.logo = request.FILES['logo']

            print organization.logo

            organization.save()

            return HttpResponseRedirect("/organizaciones")
    else:
        data = {
            'name': organization.name,
            'country': organization.country,
            'homepage': organization.homepage,
            'logo': organization.logo,
        }

        form = OrganizationForm(initial = data)

    return render_to_response("organization_manager/edit.html", {
            "organization": organization,
            "form": form,
        },
        context_instance = RequestContext(request))

def delete_organization(request, slug):
    organization = get_object_or_404(Organization, slug = slug)
    organization.delete()
    organizations = Organization.objects.all()

    return redirect('organization_index')
