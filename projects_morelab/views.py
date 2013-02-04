# coding: utf-8

from django.shortcuts import render_to_response, redirect
from django.contrib.auth import authenticate, login, logout

# Create your views here.

#########################
# View: home
#########################


def home(request):
    return render_to_response('projects_morelab/index.html')


#########################
# View: logout
#########################


def logout(request):
    logout(request)
    # Redirect to a success page.
    return render_to_response('projects_morelab/index.html')


#########################
# View: login
#########################


def login(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return render_to_response('projects_morelab/index.html')
    else:
            return redirect("http://google.es")
