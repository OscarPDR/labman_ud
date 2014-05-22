# coding: utf-8

import threading
import weakref

from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify
from django.contrib.syndication.views import Feed

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

def _validate_term(token, name, numeric = False):
    if not token.startswith(name):
        return False

    remainder = token[len(name):]
    if not remainder:
        return False
    
    if numeric:
        try:
            int(remainder)
        except:
            return False

    return True
        

def publication_index(request, tag_slug=None, publication_type_slug=None, query_string=None):
    tag = None
    publication_type = None

    clean_index = False

    if tag_slug:
        tag = Tag.objects.get(slug=tag_slug)
        publication_ids = PublicationTag.objects.filter(tag=tag).values('publication_id')
        publications = Publication.objects.filter(id__in=publication_ids).select_related('publication_type', 'authors__author').prefetch_related('authors')

    if publication_type_slug:
        publication_type = PublicationType.objects.get(slug=publication_type_slug)
        publications = Publication.objects.filter(publication_type=publication_type.id).select_related('publication_type', 'authors__author').prefetch_related('authors')

    if not tag_slug and not publication_type_slug:
        clean_index = True
        publications = Publication.objects.all().select_related('publication_type', 'authors__author').prefetch_related('authors')

    publications = publications.order_by('-year', '-title').exclude(authors=None)

    if request.method == 'POST':
        form = PublicationSearchForm(request.POST)
        if form.is_valid():
            query_string = form.cleaned_data['text']
            return HttpResponseRedirect(reverse('view_publication_query', kwargs={'query_string': query_string}))

    else:
        form = PublicationSearchForm()

    if query_string:
        # Given a query_string such as: author:"Oscar Pena" my "title word"; split in ['author:"Oscar Peña"','my','"title word"']
        initial_tokens = query_string.lower().split()
        tokens = []
        quotes_open = False
        current_token = ""
        for token in initial_tokens:
            if token.count('"') % 2 != 0:
                if quotes_open:
                    # Close quotes
                    current_token += " " + token
                    tokens.append(current_token)
                    quotes_open = False
                else:
                    current_token += token
                    quotes_open = True
            else:
                if quotes_open:
                    current_token += " " + token
                else:
                    tokens.append(token)
        if current_token:
            tokens.append(current_token)

        # Create filters that reduce the query size
        NUMERIC_FILTERS = {
            'year:' : []
        }
        FILTERS = {
            'author:' : [],
            'tag:' : [],
            'title:' : [],
        }
        special_tokens = []
        new_tokens = [] # E.g. 'author:"Aitor Almeida"' is converted to 'Aitor Almeida'
        for token in tokens:
            validated = False
            for word in FILTERS:
                if _validate_term(token, word):
                    special_tokens.append(token)
                    new_token = token[len(word):]
                    if new_token.startswith('"') and new_token.endswith('"'):
                        new_token = new_token[1:-1]
                    FILTERS[word].append(new_token)
                    new_tokens.append(new_token)
                    validated = True
                    break

            if not validated:
                for word in NUMERIC_FILTERS:
                    if _validate_term(token, word):
                        new_token = token[len(word):]
                        if new_token.startswith('"') and new_token.endswith('"'):
                            new_token = new_token[1:-1]
                        new_tokens.append(new_token)
                        NUMERIC_FILTERS[word].append(new_token)
                        special_tokens.append(token)
                        break
                    
        search_terms = [ token for token in tokens if token not in special_tokens ] + new_tokens
        
        # Filter by publication
        if special_tokens:
            sql_query = Publication.objects.all()
            for year in NUMERIC_FILTERS['year:']:
                sql_query = sql_query.filter(year = int(year))
            for title in FILTERS['title:']:
                sql_query = sql_query.filter(title__icontains = title)
            if FILTERS['tag:']:
                for tag in FILTERS['tag:']:
                    tag_ids = PublicationTag.objects.filter(tag__name__icontains = tag).select_related('tag').values('tag__id')
                    sql_query = sql_query.filter(tags__id__in=tag_ids)
            if FILTERS['author:']:
                for author in FILTERS['author:']:
                    author_ids = PublicationAuthor.objects.filter(author__full_name__icontains = author).select_related('author').values('author__id')
                    sql_query = sql_query.filter(authors__id__in=author_ids)
        else:
            sql_query = Publication.objects.all()

        sql_query = sql_query.select_related('publication_type', 'authors__author', 'tags__tag').prefetch_related('authors', 'tags','publicationauthor_set','publicationauthor_set__author')
        publication_strings = [ (publication, publication.display_all_fields().lower()) for publication in sql_query ]
        
        publications = []
        for publication, publication_string in publication_strings:
            matches = True
            for search_term in search_terms:
                if search_term not in publication_string:
                    matches = False
                    break
            if matches:
                publications.append(publication)

        clean_index = False

    publications_length = len(publications)

    last_created = Publication.objects.order_by('-log_created')[0]
    last_modified = Publication.objects.order_by('-log_modified')[0]

    # dictionary to be returned in render_to_response()
    return_dict = {
        'web_title': u'Publications',
        'clean_index': clean_index,
        'form': form,
        'last_created': last_created,
        'last_modified': last_modified,
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
    return_dict = __build_publication_return_dict(publication)
    return_dict['current_tab'] = u'info'
    return_dict['web_title'] = publication.title
    return render_to_response('publications/info.html', return_dict, context_instance=RequestContext(request))


def publication_related_projects(request, slug):
    publication = get_object_or_404(Publication, slug=slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['current_tab'] = 'projects'
    return_dict['web_title'] = u'%s - Related projects' % publication.title
    return render_to_response('publications/related_projects.html', return_dict, context_instance=RequestContext(request))


def publication_related_publications(request, slug):
    publication = get_object_or_404(Publication, slug=slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['current_tab'] = 'publications'
    return_dict['web_title'] = u'%s - Related publications' % publication.title
    return render_to_response('publications/related_publications.html', return_dict, context_instance=RequestContext(request))


def __build_publication_return_dict(publication):
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
    return {
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


###########################################################################
# Feed: publications feeds
###########################################################################

class LatestPublicationsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestPublicationsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    title = "MORElab publications"
    description = "MORElab publications"

    def get_object(self, request):
        self.__request.request = weakref.proxy(request)
        return super(LatestPublicationsFeed, self).get_object(request)

    def link(self, obj):
        url = reverse('publication_index')
        return self.__request.request.build_absolute_uri(url)

    def items(self):
        return Publication.objects.order_by('-log_created')[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract

    def item_link(self, item):
        url = reverse('publication_info', args=[item.slug or 'no-slug-found'])
        return self.__request.request.build_absolute_uri(url)
