# coding: utf-8

from django.shortcuts import render_to_response
from django.contrib.auth import logout

# Create your views here.


#########################
# View: home
#########################

def home(request):
    return render_to_response('projects_morelab/index.html')


#########################
# View: logout
#########################

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render_to_response('projects_morelab/index.html')
