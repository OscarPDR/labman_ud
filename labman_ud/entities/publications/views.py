# -*- coding: utf-8 -*-

import threading
import weakref
import re

# from django.template.defaultfilters import slugify
from django.core import serializers
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

###		publication_index
####################################################################################################

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

    form_from_year = None
    form_from_range = None
    form_to_year = None
    form_to_range = None
    form_publication_types = None
    form_tags = None
    form_authors_name = []
    form_editors_name = []

    clean_index = False

    request.session['max_publication_year'] = MAX_YEAR_LIMIT
    request.session['min_publication_year'] = MIN_YEAR_LIMIT

    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        publication_ids = PublicationTag.objects.filter(tag=tag).values('publication_id')
        publications = Publication.objects.filter(id__in=publication_ids).prefetch_related('authors')

    if publication_type:
        publications = Publication.objects.filter(child_type=publication_type)

    if not tag_slug and not publication_type:
        clean_index = True
        publications = Publication.objects.all().prefetch_related('authors')

    publications = publications.order_by('-year', '-title').exclude(authors=None)

    if request.method == 'POST':
        form_author_field_count = request.POST.get('author_field_count')
        form_editor_field_count = request.POST.get('editor_field_count')

        form = PublicationSearchForm(request.POST, extra_author=form_author_field_count,
            extra_editor=form_editor_field_count)
        if form.is_valid():
            #query_string = form.cleaned_data['text']

            query_string = form.cleaned_data['text']
            form_from_year = form.cleaned_data['from_year']
            form_from_range = form.cleaned_data['from_range']
            form_to_year = form.cleaned_data['to_year']
            form_to_range = form.cleaned_data['to_range']
            form_publication_types = form.cleaned_data['publication_types']
            form_tags = form.cleaned_data['tags']

            
            for my_tuple in reversed(form.fields.items()):
                if my_tuple[0].startswith('editor_name_'):
                    form_editor_name = form.cleaned_data[my_tuple[0]]
                    if form_editor_name:
                        form_editors_name.append(form_editor_name)
                elif my_tuple[0].startswith('author_name_'):
                    form_author_name = form.cleaned_data[my_tuple[0]]
                    if form_author_name:
                        form_authors_name.append(form_author_name)
                elif not my_tuple[0].startswith('editor_name_'):
                    break
            

            if form_from_year:
                if form_from_range == '<':
                    publications = publications.filter(year__lt=form_from_year)
                elif form_from_range == '<=':
                    publications = publications.filter(year__lte=form_from_year)
                elif form_from_range == '>':
                    publications = publications.filter(year__gt=form_from_year)
                elif form_from_range == '>=':
                    publications = publications.filter(year__gte=form_from_year)
                elif form_from_range == '==':
                    publications = publications.filter(year=form_from_year)

            if form_to_year:
                if form_to_range == '<':
                    publications = publications.filter(year__lt=form_to_year)
                elif form_to_range == '<=':
                    publications = publications.filter(year__lte=form_to_year)

            if form_publication_types:
                publications = publications.filter(child_type__in=form_publication_types)

            if form_tags:
                publications = publications.filter(publicationtag__tag__name__in=form_tags)

            found = True

            if form_authors_name:
                group_publication = []
                for name in form_authors_name:
                    person_id = Person.objects.filter(slug__contains=slugify(name)).values_list('id', flat=True)
                    if person_id and found:
                        person_publications_set = set()
                        for _id in person_id:
                            person_publications = PublicationAuthor.objects.all().filter(author_id=_id).values_list('publication_id', flat=True)
                            if person_publications:
                                person_publications_set.update(person_publications)
                        group_publication.append(person_publications_set)
                    else:
                        found = False
                if group_publication and found:
                    publications = publications.filter(id__in=list(set.intersection(*group_publication)))

            if form_editors_name:
                group_publication = []
                for name in form_editors_name:
                    person_id = Person.objects.filter(slug__contains=slugify(name)).values_list('id', flat=True)
                    if person_id and found:
                        person_publications_set = set()
                        for _id in person_id:
                            print PublicationEditor.objects.all().values_list('editor__full_name', flat=True)
                            person_publications = PublicationEditor.objects.all().filter(editor_id=_id).values_list('publication_id', flat=True)
                            if person_publications:
                                person_publications_set.update(person_publications)
                        group_publication.append(person_publications_set)
                    else:
                        found = False
                if group_publication and found:
                    publications = publications.filter(id__in=list(set.intersection(*group_publication)))

            if not found:
                publications = []

            session_filter_dict = {
                'query_string' : query_string,
                'publications': serializers.serialize('json', publications),
                'form_from_year' : form_from_year,
                'form_from_range' : form_from_range,
                'form_to_year' : form_to_year,
                'form_to_range' : form_to_range,
                'form_publication_types' : form_publication_types,
                'form_tags' : form_tags,
                'form_authors_name' : form_authors_name,
                'form_editors_name' : form_editors_name,
                'form_author_field_count' : len(form_authors_name),
                'form_editor_field_count' : len(form_editors_name),
            }

            request.session['filtered'] = session_filter_dict

            return HttpResponseRedirect(reverse('filtered_publication_query'))

    else:
        if 'filtered' in request.session.keys():
            p = re.compile(ur'publications\/filtered(\/\?page=[1-9]+)?')

            if re.search(p, request.path) == None:
                # IF requested page is not filted, deletes session filter info.
                del request.session['filtered']
                # Loads default report.
                form = PublicationSearchForm(extra_author=1, extra_editor=1)
            else:
                # IF requested page is filtered, loads info from session.
                author_field_count = request.session['filtered']['form_author_field_count']
                editor_field_count = request.session['filtered']['form_editor_field_count']
                if author_field_count == 0:
                    author_field_count = 1
                if editor_field_count == 0:
                    editor_field_count = 1
                form = PublicationSearchForm(extra_author=author_field_count,
                    extra_editor=editor_field_count)
                query_string = request.session['filtered']['query_string']
                publications = []
                for deserialized_object in serializers.deserialize('json',
                    request.session['filtered']['publications']):
                    publications.append(deserialized_object.object)
                form_from_year = request.session['filtered']['form_from_year']
                form_from_range = request.session['filtered']['form_from_range']
                form_to_year = request.session['filtered']['form_to_year']
                form_to_range = request.session['filtered']['form_to_range']
                form_publication_types = []
                for utf8type in request.session['filtered']['form_publication_types']:
                    form_publication_types.append(utf8type.encode('utf8'))
                form_tags = request.session['filtered']['form_tags']
                form_authors_name = []
                for utf8type in request.session['filtered']['form_authors_name']:
                    form_authors_name.append(utf8type.encode('utf8'))
                form_editor_name = []
                for utf8type in request.session['filtered']['form_editors_name']:
                    form_editors_name.append(utf8type.encode('utf8'))
                clean_index = False
        else:
            form = PublicationSearchForm(extra_author=1, extra_editor=1)

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

        # Query by author and title
        
        # sql_query = Publication.objects.exclude(authors=None).all()
        sql_query_titles = Publication.objects.filter(title__icontains=query_string).all()
        author_ids = PublicationAuthor.objects.filter(author__full_name__icontains=query_string).values_list('author__id', flat=True)
        sql_query_authors = Publication.objects.filter(authors__in=author_ids).all()

        # Fix by Unai & Ruben S
        sql_query_titles = sql_query_titles.prefetch_related('authors', 'tags', 'publicationauthor_set', 'publicationauthor_set__author')
        sql_query_authors = sql_query_authors.prefetch_related('authors', 'tags', 'publicationauthor_set', 'publicationauthor_set__author')
        sql_query = sql_query_titles | sql_query_authors
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

    # Retrieves all the publication types.
    publications_ids = PublicationAuthor.objects.values_list('publication',
        flat=True)
    publication_types_info = Publication.objects.filter(
        id__in=publications_ids).order_by().values('child_type').distinct()

    # Retrieves all the tag names.
    tags_id_info = Publication.objects.all().values_list('tags', flat=True)
    tags_info = Tag.objects.filter(id__in=tags_id_info).order_by().values_list('name', flat=True)

    # Retrieves all the full names of authors.
    author_info = PublicationAuthor.objects.all() \
        .distinct('author__full_name').order_by() \
        .values_list('author__full_name', flat=True)

    # Retrieves all the full names of editors.
    editor_info = PublicationEditor.objects \
        .distinct('editor__full_name').order_by() \
        .values_list('editor__full_name', flat=True)

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

    try:
        theses = Thesis.objects.all()

    except:
        theses = None

    # dictionary to be returned in render(request, )
    return_dict = {
        'clean_index': clean_index,
        'form': form,
        'last_entry': last_entry,
        'author_info': author_info,
        'editor_info': editor_info,
        'publication_type': publication_type,
        'publication_types_info' : publication_types_info,
        'publications': publications,
        'publications_length': len(publications),
        'query_string': query_string,
        'tag': tag,
        'publication_tags_info' : tags_info,
        'theses': theses,
        'form_from_year' : form_from_year,
        'form_from_range' : form_from_range,
        'form_to_year' : form_to_year,
        'form_to_range' : form_to_range,
        'form_publication_types' : form_publication_types,
        'form_tags' : form_tags,
        'form_authors_name' : form_authors_name,
        'form_editors_name' : form_editors_name,
        'web_title': u'Publications',
    }

    return render(request, 'publications/index.html', return_dict)

###		publication_info
####################################################################################################

def publication_info(request, publication_slug):
    publication = get_object_or_404(Publication, slug=publication_slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['web_title'] = publication.title
    return render(request, 'publications/info.html', return_dict)


def publication_ext_info(request, publication_slug):
    publication = get_object_or_404(Publication, slug=publication_slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['web_title'] = publication.title
    return render(request, 'publications/extended_info.html', return_dict)


def publication_related_projects(request, publication_slug):
    publication = get_object_or_404(Publication, slug=publication_slug)
    return_dict = __build_publication_return_dict(publication)
    return_dict['web_title'] = u'%s - Related projects' % publication.title
    return render(request, 'publications/related_projects.html', return_dict)


def publication_related_publications(request, publication_slug):
    publication = get_object_or_404(Publication, slug=publication_slug)
    return_dict = __build_publication_return_dict(publication)
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


####################################################################################################
# Feed: publications feeds
####################################################################################################

class LatestPublicationsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestPublicationsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    try:
        _settings = LabmanDeployGeneralSettings.objects.get()
        research_group_short_name = _settings.research_group_short_name

    except:
        research_group_short_name = u'Our'

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

###		phd_dissertations_index
####################################################################################################

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
