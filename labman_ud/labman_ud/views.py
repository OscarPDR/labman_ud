# coding: utf-8

from django.shortcuts import render_to_response
from django.contrib.auth import logout
from django.template import RequestContext

from entities.news.models import News


# Create your views here.


#########################
# View: home
#########################

def home(request):
    last_news = News.objects.order_by('-created')[:3]

    return render_to_response('labman_ud/index.html', {
            'last_news': last_news,
        },
        context_instance=RequestContext(request))


#########################
# View: logout
#########################

def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return render_to_response('labman_ud/index.html')


#########################
# View: about
#########################

def about(request):
    return render_to_response('labman_ud/about.html')


#########################
# View: view404
#########################

def view404(request):
    return render_to_response('labman_ud/404.html')
