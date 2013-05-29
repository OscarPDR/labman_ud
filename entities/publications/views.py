# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import Publication
from .forms import PublicationSearchForm

# Create your views here.

PAGINATION_NUMBER = settings.PUBLICATIONS_PAGINATION


#########################
# View: publication_index
#########################

def publication_index(request):
    publications = Publication.objects.all().order_by('title')

    if request.method == 'POST':
        form = PublicationSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            pubs = []

            for publication in publications:
                if query in publication.slug:
                    pubs.append(publication)

            publications = pubs

    else:
        form = PublicationSearchForm()

    paginator = Paginator(publications, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        publications = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        publications = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        publications = paginator.page(paginator.num_pages)

    return render_to_response('publications/index.html', {
            'publications': publications,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: publication_info
#########################

def publication_info(request, slug):
    # from_page = ''

    # http_referer = request.META['HTTP_REFERER']

    # if '?page=' in http_referer:
    #     from_page = http_referer[http_referer.rfind('/')+1:]

    # person = get_object_or_404(Person, slug=slug)

    # projects = {}

    # roles = Role.objects.all()

    # for role in roles:
    #     projects[role.name] = []
    #     project_ids = AssignedPerson.objects.filter(person_id=person.id, role=role.id).values('project_id')
    #     project_objects = Project.objects.filter(id__in=project_ids).order_by('slug')
    #     for project in project_objects:
    #         projects[role.name].append(project)

    return render_to_response('publications/info.html', {
        },
        context_instance=RequestContext(request))
