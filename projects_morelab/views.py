# coding: utf-8

from django.shortcuts import render_to_response

# Create your views here.

#########################
# View: home
#########################


def home(request):
    return render_to_response('projects_morelab/index.html')
