# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings

from .models import Publication, PublicationAuthor, PublicationTag, PublicationType
from .forms import PublicationSearchForm

from entities.projects.models import Project, RelatedPublication

from entities.persons.models import Person

from entities.utils.models import Tag


# Create your views here.

PAGINATION_NUMBER = settings.PUBLICATIONS_PAGINATION


#########################
# View: publication_index
#########################

def publication_index(request):
    publications = Publication.objects.all().order_by('title')

    publications_length = len(publications)

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
            'publications_length': publications_length,
        },
        context_instance=RequestContext(request))


#########################
# View: publication_info
#########################

def publication_info(request, slug):
    from_page = ''

    http_referer = request.META['HTTP_REFERER']

    if '?page=' in http_referer:
        from_page = http_referer[http_referer.rfind('/')+1:]

    publication = get_object_or_404(Publication, slug=slug)

    author_ids = PublicationAuthor.objects.filter(publication=publication.id).values('author_id').order_by('position')
    authors = []

    for _id in author_ids:
        author = Person.objects.get(id=_id['author_id'])
        authors.append(author)

    related_projects_ids = RelatedPublication.objects.filter(publication=publication.id).values('project_id')
    related_projects = Project.objects.filter(id__in=related_projects_ids)

    related_publications_ids = RelatedPublication.objects.filter(project_id__in=related_projects_ids).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).exclude(id=publication.id)

    tag_ids = PublicationTag.objects.filter(publication=publication.id).values('tag_id')
    tags = Tag.objects.filter(id__in=tag_ids)
    tags = tags.extra(select={'length': 'Length(tag)'}).order_by('length')

    return render_to_response('publications/info.html', {
            'from_page': from_page,
            'publication': publication,
            'authors': authors,
            'related_projects': related_projects,
            'related_publications': related_publications,
            'tags': tags,
        },
        context_instance=RequestContext(request))


#########################
# View: view_tag
#########################

def view_publication_tag(request, tag_slug):
    tag = Tag.objects.get(slug=tag_slug)

    publication_ids = PublicationTag.objects.filter(tag=tag).values('publication_id')
    publications = Publication.objects.filter(id__in=publication_ids).order_by('title')

    paginator = Paginator(publications, PAGINATION_NUMBER)

    page = request.GET.get('page')

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
            'tag': tag,
        },
        context_instance=RequestContext(request))


#########################
# View: view_publication_type
#########################

def view_publication_type(request, publication_type_slug):
    publication_type = PublicationType.objects.get(slug=publication_type_slug)

    publications = Publication.objects.filter(publication_type=publication_type.id).order_by('-published')

    paginator = Paginator(publications, PAGINATION_NUMBER)

    page = request.GET.get('page')

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
            'publication_type': publication_type,
        },
        context_instance=RequestContext(request))


#########################
# View: publication_tag_cloud
#########################

def publication_tag_cloud(request):

    tag_dict = {}

    tags = PublicationTag.objects.all()

    for tag in tags:
        t = tag.tag.tag
        if t in tag_dict.keys():
            tag_dict[t] = tag_dict[t] + 1
        else:
            tag_dict[t] = 1

    return render_to_response('publications/tag_cloud.html', {
            'tag_dict': tag_dict,
        },
        context_instance=RequestContext(request))
