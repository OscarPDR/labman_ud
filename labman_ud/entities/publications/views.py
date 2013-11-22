# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from .forms import PublicationSearchForm
from .models import Publication, PublicationAuthor, PublicationTag, PublicationType

from entities.persons.models import Person
from entities.projects.models import Project, RelatedPublication
from entities.utils.models import Tag


# Create your views here.

INDICATORS_TAG_SLUGS = ['isi', 'corea', 'coreb', 'corec', 'q1', 'q2', 'q3', 'q4']


###########################################################################
# View: publication_index
###########################################################################

def publication_index(request, tag_slug=None, publication_type_slug=None, query_string=None):
    tag = None
    publication_type = None

    clean_index = False

    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        publication_ids = PublicationTag.objects.filter(tag=tag).values('publication_id')
        publications = Publication.objects.filter(id__in=publication_ids)

    if publication_type_slug:
        publication_type = PublicationType.objects.get(slug=publication_type_slug)
        publications = Publication.objects.filter(publication_type=publication_type.id)

    if not tag_slug and not publication_type_slug:
        clean_index = True
        publications = Publication.objects.all()

    publications = publications.order_by('-year', '-title').exclude(authors=None)

    if request.method == 'POST':
        form = PublicationSearchForm(request.POST)
        if form.is_valid():
            query_string = form.cleaned_data['text']

            return HttpResponseRedirect(reverse('view_publication_query', kwargs={'query_string': query_string}))

    else:
        form = PublicationSearchForm()

    if query_string:
        query = slugify(query_string)

        pubs = []

        person_ids = Person.objects.filter(slug__contains=query).values('id')
        publication_ids = PublicationAuthor.objects.filter(author_id__in=person_ids).values('publication_id')
        publication_ids = set([x['publication_id'] for x in publication_ids])

        for publication in publications:
            if (query in slugify(publication.title)) or (publication.id in publication_ids):
                pubs.append(publication)

        publications = pubs
        clean_index = False

    publications_length = len(publications)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'publication_type': publication_type,
        'publications': publications,
        'publications_length': publications_length,
        'query_string': query_string,
        'tag': tag,
    }

    return render_to_response('publications/index.html', return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publication_info
###########################################################################

def publication_info(request, slug):

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
    tags = Tag.objects.filter(id__in=tag_ids).order_by('name')

    tag_list = []
    indicators_list = []

    for tag in tags:
        if tag.slug in INDICATORS_TAG_SLUGS:
            indicators_list.append(tag)
        else:
            tag_list.append(tag)

    try:
        pdf = publication.pdf
    except:
        pdf = None

    try:
        parent_publication = Publication.objects.get(id=publication.part_of.id)
    except:
        parent_publication = None

    bibtex = publication.bibtex.replace(",", ",\n")

    # dictionary to be returned in render_to_response()
    return_dict = {
        'authors': authors,
        'bibtex': bibtex,
        'indicators_list': indicators_list,
        'parent_publication': parent_publication,
        'pdf': pdf,
        'publication': publication,
        'related_projects': related_projects,
        'related_publications': related_publications,
        'tag_list': tag_list,
    }

    return render_to_response('publications/info.html', return_dict, context_instance=RequestContext(request))


###########################################################################
# View: publication_tag_cloud
###########################################################################

def publication_tag_cloud(request):

    tag_dict = {}

    tags = PublicationTag.objects.all()

    for tag in tags:
        t = tag.tag.name
        if t in tag_dict.keys():
            tag_dict[t] = tag_dict[t] + 1
        else:
            tag_dict[t] = 1

    # dictionary to be returned in render_to_response()
    return_dict = {
        'tag_dict': tag_dict,
    }

    return render_to_response('publications/tag_cloud.html', return_dict, context_instance=RequestContext(request))
