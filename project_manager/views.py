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
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            cd = form.cleaned_data

            project_type = cd['project_type']
            title = cd['title']
            description = cd['description']
            homepage = cd['homepage']
            start_year = cd['start_year']
            end_year = cd['end_year']
            status = cd['status']
            currency = cd['currency']
            observations = cd['observations']

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

            if request.FILES['logo']:
                project.logo = request.FILES['logo']

            project.save()

            return HttpResponseRedirect("/correct")
    else:
        form = ProjectForm()

    return render_to_response("project_manager/add.html", {"form": form, }, context_instance=RequestContext(request))


def delete_project(request, slug):
    project = get_object_or_404(Project, slug = slug)
    project.delete()

    return redirect('project_index')
