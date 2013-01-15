# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from project_manager.models import *
from project_manager.forms import *


def project_index(request):
    return render_to_response("project_manager/index.html", {}, context_instance=RequestContext(request))


def add_project(request):
    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            project_type = cd['project_type']
            title = cd['title']

            project = Project(
                project_type = project_type.encode('utf-8'),
                title = title.encode('utf-8')
            )

            project.save()

            return HttpResponseRedirect("/projects")
    else:
        form = ProjectForm()

    return render_to_response("project_manager/add.html", {"form": form, }, context_instance=RequestContext(request))
