
from django.contrib.auth import logout
from django.shortcuts import render, redirect
from django.template import RequestContext

from entities.news.models import News
from labman_setup.models import AboutSection


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


###     logout_view()
####################################################################################################

def logout_view(request):
    logout(request)

    return redirect('home')


###     about_info(about_page_slug)
####################################################################################################

def about_info(request, about_page_slug):
    if about_page_slug == u'collaborations':
        about_section = None
        title = u'Collaborations'
        collaborations = True

    else:
        about_section = AboutSection.objects.get(slug=about_page_slug)
        title = about_section.title
        collaborations = False

    return_dict = {
        'about_section': about_section,
        'collaborations': collaborations,
        'web_title': u'About - %s' % title,
    }

    return render(request, 'labman_ud/about_info.html', return_dict)


###     view404()
####################################################################################################

def view404(request):
    return render(request, 'labman_ud/404.html')
