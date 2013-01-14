# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from project_manager.models import *
from project_manager.forms import *


def project_index(request):
    form = ProjectForm()

    if request.POST:
        form = ProjectForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/added")
        else:
            form = ProjectForm()

    return render_to_response("projects_morelab/index.html", {"form": form, }, context_instance=RequestContext(request))
