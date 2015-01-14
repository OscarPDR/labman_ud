
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.template import RequestContext

from entities.news.models import News
from labman_setup.models import AboutSection


####################################################################################################
###     home()
####################################################################################################

def home(request):
    if RequestContext(request).get('INITIAL_SETUP'):
        return render(request, 'labman_ud/initial_setup.html', {})

    else:
        # dictionary to be returned in render(request, )
        return_dict = {
            'latest_news': News.objects.order_by('-created')[:3],
        }

        return render(request, 'labman_ud/index.html', return_dict)


####################################################################################################
###     logout_view()
####################################################################################################

def logout_view(request):
    logout(request)

    return redirect('home')


####################################################################################################
###     about()
####################################################################################################

def about(request):
    about_sections = AboutSection.objects.all().order_by('order')

    return_dict = {
        'web_title': u'About',
        'about_sections': about_sections,
    }

    return render(request, 'labman_ud/about.html', return_dict)


####################################################################################################
###     about_collaborations()
####################################################################################################

def about_collaborations(request):
    return render(request, 'labman_ud/about/collaborations.html', {'web_title': 'Collaborations'})


####################################################################################################
###     about_prototyping()
####################################################################################################

def about_prototyping(request):
    return render(request, 'labman_ud/about/prototyping.html', {'web_title': 'Prototyping'})


####################################################################################################
###     view404()
####################################################################################################

def view404(request):
    return render(request, 'labman_ud/404.html')
