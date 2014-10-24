
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template import RequestContext

from entities.news.models import News


# Create your views here.


###########################################################################
# View: home
###########################################################################

def home(request):
    if RequestContext(request).get('INITIAL_SETUP'):
        return render(request, 'labman_ud/initial_setup.html', {})

    else:
        # dictionary to be returned in render(request, )
        return_dict = {
            'latest_news': News.objects.order_by('-created')[:3],
        }

        return render(request, 'labman_ud/index.html', return_dict)


###########################################################################
# View: logout
###########################################################################

def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


###########################################################################
# View: about
###########################################################################

def about(request):
    return render(request, 'labman_ud/about.html', {'web_title': 'About'})


###########################################################################
# View: about_collaborations
###########################################################################

def about_collaborations(request):
    return render(request, 'labman_ud/about/collaborations.html', {'web_title': 'Collaborations'})


###########################################################################
# View: about_prototyping
###########################################################################

def about_prototyping(request):
    return render(request, 'labman_ud/about/prototyping.html', {'web_title': 'Prototyping'})


###########################################################################
# View: view404
###########################################################################

def view404(request):
    return render(request, 'labman_ud/404.html')
