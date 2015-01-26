# -*- encoding: utf-8 -*-

import threading
import weakref

# from django.template.defaultfilters import slugify
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404

from .forms import PublicationSearchForm
from .models import *

from entities.persons.models import Person
from entities.projects.models import Project, RelatedPublication
from entities.utils.models import Tag

from labman_setup.models import *
from labman_ud.util import *

from collections import OrderedDict, Counter


###########################################################################
# View: publication_index
###########################################################################

def _validate_term(token, name, numeric=False):
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


def publication_index(request, tag_slug=None, publication_type=None, query_string=None):
    tag = None

    clean_index = False

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        publication_ids = PublicationTag.objects.filter(tag=tag).values('publication_id')
        publications = Publication.objects.filter(id__in=publication_ids).select_related('authors__author').prefetch_related('authors')

    if publication_type:
        publications = Publication.objects.filter(child_type=publication_type)

    if not tag_slug and not publication_type:
        clean_index = True
        publications = Publication.objects.all().select_related('authors__author').prefetch_related('authors')

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
            'year:': []
        }

        FILTERS = {
            'author:': [],
            'tag:': [],
            'title:': [],
        }

        special_tokens = []
        new_tokens = []  # E.g. 'author:"Aitor Almeida"' is converted to 'Aitor Almeida'
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

        search_terms = [token for token in tokens if token not in special_tokens] + new_tokens

        # Filter by publication
        if special_tokens:
            sql_query = Publication.objects.exclude(authors=None).all()

            for year in NUMERIC_FILTERS['year:']:
                sql_query = sql_query.filter(year=int(year))

            for title in FILTERS['title:']:
                sql_query = sql_query.filter(title__icontains=title)

            if FILTERS['tag:']:
                for tag in FILTERS['tag:']:
                    tag_ids = PublicationTag.objects.filter(tag__name__icontains=tag).select_related('tag').values('tag__id')
                    sql_query = sql_query.filter(tags__id__in=tag_ids)

            if FILTERS['author:']:
                for author in FILTERS['author:']:
                    author_ids = PublicationAuthor.objects.filter(author__full_name__icontains=author).select_related('author').values('author__id')
                    sql_query = sql_query.filter(authors__id__in=author_ids)
        else:
            sql_query = Publication.objects.exclude(authors=None).all()

        sql_query = sql_query.select_related('authors__author', 'tags__tag').prefetch_related('authors', 'tags', 'publicationauthor_set', 'publicationauthor_set__author')
        publication_strings = [(publication, publication.display_all_fields().lower()) for publication in sql_query]

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

    publication_model_list = [
        'Book',
        'BookSection',
        'ConferencePaper',
        'Journal',
        'JournalArticle',
        'Magazine',
        'MagazineArticle',
        'Proceedings',
        'Publication',
        'Thesis',
    ]

    last_entry = get_last_model_update_log_entry('publications', publication_model_list)

    publication_types = Publication.objects.all().exclude(authors=None).values_list('child_type', flat=True)

    counter = Counter(publication_types)
    ord_dict = OrderedDict(sorted(counter.items(), key=lambda t: t[1]))

    items = ord_dict.items()

    try:
        theses = Thesis.objects.all()

    except:
        theses = None

    # dictionary to be returned in render(request, )
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'last_entry': last_entry,
        'publication_type': publication_type,
        'publications': publications,
        'publications_length': publications_length,
        'pubtype_info': dict(items),
        'query_string': query_string,
        'tag': tag,
        'theses': theses,
        'web_title': u'Publications',
    }

    return render(request, 'publications/index.html', return_dict)


###########################################################################
# View: publication_info
###########################################################################

def publication_info(request, slug):
    publication = get_object_or_404(Publication, slug=slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['current_tab'] = u'info'
    return_dict['web_title'] = publication.title
    return render(request, 'publications/info.html', return_dict)


def publication_related_projects(request, slug):
    publication = get_object_or_404(Publication, slug=slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['current_tab'] = 'projects'
    return_dict['web_title'] = u'%s - Related projects' % publication.title
    return render(request, 'publications/related_projects.html', return_dict)


def publication_related_publications(request, slug):
    publication = get_object_or_404(Publication, slug=slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['current_tab'] = 'publications'
    return_dict['web_title'] = u'%s - Related publications' % publication.title
    return render(request, 'publications/related_publications.html', return_dict)


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
    tag_list = Tag.objects.filter(id__in=tag_ids).order_by('name')

    try:
        pdf = publication.pdf
    except:
        pdf = None

    parent_publication = None

    try:
        if publication.child_type == 'ConferencePaper':
            publication = ConferencePaper.objects.get(slug=publication.slug)
            parent_publication = Proceedings.objects.get(id=publication.parent_proceedings.id)

        if publication.child_type == 'JournalArticle':
            publication = JournalArticle.objects.get(slug=publication.slug)
            parent_publication = Journal.objects.get(id=publication.parent_journal.id)

        if publication.child_type == 'MagazineArticle':
            publication = MagazineArticle.objects.get(slug=publication.slug)
            parent_publication = Magazine.objects.get(id=publication.parent_magazine.id)

        if publication.child_type == 'BookSection':
            publication = BookSection.objects.get(slug=publication.slug)
            parent_publication = Book.objects.get(id=publication.parent_book.id)

        if publication.child_type == 'Book':
            publication = Book.objects.get(slug=publication.slug)
            parent_publication = None

    except:
        pass

    if publication.bibtex:
        bibtex = publication.bibtex.replace(",", ",\n")
    else:
        bibtex = None

    rankings = set()

    try:
        for publication_rank in PublicationRank.objects.filter(publication=publication):
            rankings.add(publication_rank.ranking)

    except:
        pass

    if parent_publication:
        try:
            for publication_rank in PublicationRank.objects.filter(publication=parent_publication):
                rankings.add(publication_rank.ranking)

        except:
            pass

    # dictionary to be returned in render(request, )
    return {
        'authors': authors,
        'bibtex': bibtex,
        'parent_publication': parent_publication,
        'pdf': pdf,
        'publication': publication,
        'rankings': list(rankings),
        'related_projects': related_projects,
        'related_publications': related_publications,
        'tag_list': tag_list,
    }


###########################################################################
# View: publication_tag_cloud
###########################################################################

def publication_tag_cloud(request):
    tags = PublicationTag.objects.all().values_list('tag__name', flat=True)

    counter = Counter(tags)
    ord_dict = OrderedDict(sorted(counter.items(), key=lambda t: t[1]))

    items = ord_dict.items()
    items = items[len(items)-100:]

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'Publications tag cloud',
        'tag_dict': dict(items),
    }

    return render(request, 'publications/tag_cloud.html', return_dict)


###########################################################################
# Feed: publications feeds
###########################################################################

class LatestPublicationsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestPublicationsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    _settings = LabmanDeployGeneralSettings.objects.get()
    research_group_short_name = _settings.research_group_short_name

    title = u'%s publications' % research_group_short_name
    description = u'%s publications' % research_group_short_name

    def get_object(self, request):
        self.__request.request = weakref.proxy(request)
        return super(LatestPublicationsFeed, self).get_object(request)

    def link(self, obj):
        url = reverse('publication_index')
        return self.__request.request.build_absolute_uri(url)

    def items(self):
        return Publication.objects.order_by('-id')[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.abstract

    def item_link(self, item):
        url = reverse('publication_info', args=[item.slug or 'no-slug-found'])
        return self.__request.request.build_absolute_uri(url)


###########################################################################
# View: phd_dissertations_index
###########################################################################

def phd_dissertations_index(request):

    phd_dissertations = []

    theses = Thesis.objects.order_by('-viva_date', 'author__full_name')

    for thesis in theses:
        phd_dissertation = {}

        phd_dissertation['thesis'] = thesis

        co_advisors = CoAdvisor.objects.filter(thesis=thesis)

        if co_advisors:
            phd_dissertation['co_advisors'] = []

            for co_advisor in co_advisors:
                phd_dissertation['co_advisors'].append(co_advisor.co_advisor.full_name)

        phd_dissertations.append(phd_dissertation)

    # dictionary to be returned in render(request, )
    return_dict = {
        'web_title': u'PhD dissertations',
        'phd_dissertations': phd_dissertations,
    }

    return render(request, 'publications/phd_dissertations_index.html', return_dict)
