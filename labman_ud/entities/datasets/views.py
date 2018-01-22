# -*- encoding: utf-8 -*-

from django.shortcuts import render, get_object_or_404
from django.template.defaultfilters import slugify
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.db.models import Sum, Min, Max

from .models import *
from .forms import *

from entities.persons.models import Person
from entities.projects.models import Project
from labman_ud.util import *

import re
import datetime

###     datasets_index()
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


def datasets_index(request, tag_slug=None):
    """
    This method load the index page of datasets. The idea of this method is to make a select into DB to obtain
    the needed information about the stored databsets and show it in a table

    :param request: POST or GET request
    :param tag_slug:
    :param query_string: The type of query used in the filter.
    :return: A python dict to the template
    """

    # Setting datasets maximun time differences
    request.session['max_dataset_year'] = MAX_YEAR_LIMIT
    request.session['min_dataset_year'] = MIN_YEAR_LIMIT

    if request.method == 'POST':
        # We are performing a filtering operation, catch data and make a reverse pass
        # Creating the form object
        form = DatasetSearchForm(request.POST)
        # Validating the form data
        if form.is_valid():
            # Data is valid, appending needed information
            filter_data_dict = {
                'from_year': form.cleaned_data['from_year'] or None,
                'from_range': form.cleaned_data['from_range'] or None,
                'to_year': form.cleaned_data['to_year'] or None,
                'to_range': form.cleaned_data['to_range'] or None,
                'license': form.cleaned_data['license'] or None,
                'file_format': form.cleaned_data['file_format'] or None,
                'tags': form.cleaned_data['tags'] or None,
            }
            # Adding data to the session
            request.session['filter_data'] = filter_data_dict
            # Redirection fo the filtered IRL
        return HttpResponseRedirect(reverse('filtered_dataset_query'))
    else:
        # Initial variables
        tag = None
        clean_index = False
        query_string = None
        form_tags = None
        form_from_range = None
        # Obtaining session filter_data to know if we have filtering data
        filter_data = request.session.get('filter_data', None)
        # Check if we are calling to filtering page or not to avoid any session active filtering
        p = re.compile(ur'datasets\/filtered(\/\?page=[1-9]+)?')
        if tag_slug or re.search(p, request.path) is not None and filter_data:
            # We have filtering data
            if tag_slug:
                # Filtering by tag
                tag = get_object_or_404(Tag, slug=tag_slug)
                dataset_ids = DatasetTag.objects.filter(tag=tag).values('dataset_id')
                datasets = Dataset.objects.filter(id__in=dataset_ids).prefetch_related('authors')
                # Default form
                form = DatasetSearchForm()
            else:
                # Populate form with filtered data
                form = DatasetSearchForm(filter_data)
                if form.is_valid():
                    # Obtaining all objects (No filtering)
                    datasets = Dataset.objects.exclude(authors=None).all()
                    # Obtaining form values
                    # Basic text search
                    query_string = form.cleaned_data['text'] or None
                    # Advanced options
                    from_year = form.cleaned_data['from_year'] or None
                    form_from_range = form.cleaned_data['from_range'] or None
                    to_year = form.cleaned_data['to_year'] or None
                    form_to_range = form.cleaned_data['to_range'] or None
                    license = form.cleaned_data['license'] or None
                    file_format = form.cleaned_data['file_format'] or None
                    form_tags = form.cleaned_data['tags'] or None

                    ### Performing an advanced filtering
                    if license:
                        datasets = datasets.filter(license__in=license)
                    if file_format:
                        datasets = datasets.filter(format__in=file_format)
                    if form_tags:
                        datasets = datasets.filter(datasettag__tag__name__in=form_tags)
                    # Filtering by date
                    if from_year and form_from_range:
                        if form_from_range == '<':
                            # Less than
                            datasets = datasets.filter(date__lt=datetime.datetime.strptime(from_year, '%Y'))
                        elif form_from_range == '<=':
                            # Less or equal than
                            datasets = datasets.filter(date__lte=datetime.datetime.strptime(from_year, '%Y'))
                        elif form_from_range == '>' or form_from_range == '>=':
                            if form_from_range == '>':
                                # Greater than
                                datasets = datasets.filter(date__gt=datetime.datetime.strptime(from_year, '%Y'))
                            else:
                                # Greater equal than
                                datasets = datasets.filter(date__gte=datetime.datetime.strptime(from_year, '%Y'))
                            # Filtering by to_year
                            if to_year:
                                if form_to_range == '<=':
                                    # Less or equal
                                    datasets = datasets.filter(date__lte=datetime.datetime.strptime(to_year, '%Y'))
                                else:
                                    datasets = datasets.filter(date__lt=datetime.datetime.strptime(to_year, '%Y'))
                        else:
                            # Equal
                            datasets = datasets.filter(date__year=from_year)

                    ### Filterig by text
                    if query_string:
                        # Performing a partially search text
                        # Given a query_string such as: author:"Oscar Pena" my "title word"; split in
                        # ['author:"Oscar Peña"','my','"title word"']
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
                            'date:': []
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
                            sql_query = datasets

                            for date in NUMERIC_FILTERS['date:']:
                                sql_query = sql_query.filter(date=int(date))

                            for title in FILTERS['title:']:
                                sql_query = sql_query.filter(title__icontains=title)

                            if FILTERS['tag:']:
                                for tag in FILTERS['tag:']:
                                    tag_ids = DatasetTag.objects.filter(tag__name__icontains=tag).values(
                                        'tag__id')
                                    sql_query = sql_query.filter(tags__id__in=tag_ids)

                            if FILTERS['author:']:
                                for author in FILTERS['author:']:
                                    author_ids = DatasetAuthor.objects.filter(
                                        author__full_name__icontains=author).values('author__id')
                                    sql_query = sql_query.filter(authors__id__in=author_ids)
                        else:
                            sql_query = datasets

                        # Ordering datasets by list
                        sql_query = sql_query.order_by('-date', '-title').exclude(authors=None).prefetch_related \
                            ('authors', 'tags', 'datasetauthor_set', 'datasetauthor_set__author')
                        dataset_strings = [(all_datasets, all_datasets.display_all_fields().lower()) for
                                           all_datasets in sql_query]
                        # Obtaining the final matches
                        datasets = []
                        for dataset, dataset_string in dataset_strings:
                            matches = True
                            for search_term in search_terms:
                                if search_term not in dataset_string:
                                    matches = False
                                    break
                            if matches:
                                # Adding filtered matched datasets
                                datasets.append(dataset)
                else:
                    # Some error happened, removing data and giving an error
                    request.session.pop('filter_data', None)
                    datasets = list(Dataset.objects.all().prefetch_related('authors') \
                                    .order_by('-date', '-title').exclude(authors=None)) or None
        else:
            # No filtering, loading all objects and default form
            clean_index = True
            form = DatasetSearchForm()
            request.session.pop('filter_data', None)
            # Obtaining full datasets from db with ordering
            datasets = list(Dataset.objects.all().prefetch_related('authors') \
                            .order_by('-date', '-title').exclude(authors=None)) or None

        # Obtaining the last dataset entry
        dataset_model_list = ['Dataset']
        last_entry = get_last_model_update_log_entry('datasets', dataset_model_list)

        # Obtaining dataset tag information
        tags_id_info = Dataset.objects.all().values_list('tags', flat=True)
        tags_info = Tag.objects.filter(id__in=tags_id_info).order_by('name').values_list('name', flat=True)

        # Return dict to the template
        return_dict = {
            'clean_index': clean_index,
            'query_string': query_string,
            'form': form,
            'tag': tag,
            'form_tags': form_tags,
            'datasets': datasets if datasets else None,
            'dataset_tags_info': tags_info,
            'dataset_length': len(datasets) if datasets else 0,
            'last_entry': last_entry,
            'form_from_range': form_from_range,
        }
        # Rendering page
        return render(request, "datasets/index.html", return_dict)


###		dataset_info
####################################################################################################

def dataset_info(request, dataset_slug):
    """

    Extended information of the given dataset. This method builds the needed information to show
    to the request user detailed information of the dataset.

    :param request: information about the request type from the user
    :param dataset_slug: the slug name of the dataset, useful to the information from DB
    :return:
    """

    dataset = get_object_or_404(Dataset, slug=dataset_slug)
    # dictionary to be returned in render(request, )
    return_dict = __build_dataset_information(dataset)
    return_dict['web_title'] = dataset.title
    return render(request, "datasets/info.html", return_dict)


###		dataset_extended information
####################################################################################################
# def dataset_ext_info(request, dataset_slug):
#     dataset = get_object_or_404(Dataset, slug=dataset_slug)
#     # dictionary to be returned in render(request, )
#     return_dict = __build_dataset_information(dataset)
#     return_dict['web_title'] = dataset.title
#     return render(request, 'datasets/extended_info.html', return_dict)


############################################################################
# Function: __build_project_information
############################################################################

def __build_dataset_information(dataset):
    # Getting dataset tags
    tag_ids = DatasetTag.objects.filter(dataset=dataset.id).values('tag_id')
    tags = Tag.objects.filter(id__in=tag_ids).order_by('name')
    # Getting projects
    project_ids = DatasetProject.objects.filter(dataset=dataset.id).values('project_id')
    projects = Project.objects.filter(id__in=project_ids).order_by('full_name')
    # Getting dataset authors
    author_ids = DatasetAuthor.objects.filter(dataset=dataset.id).values('author_id').order_by('position')
    authors = []
    for _id in author_ids:
        author = Person.objects.get(id=_id['author_id'])
        authors.append(author)



    # dictionary to be returned in render(request, )
    return {
        'dataset': dataset,
        'year': dataset.date.year,
        'tags': tags,
        'file': dataset.file if dataset.file else None,
        'format': dataset.format,
        # 'logo': dataset.logo if dataset.logo else None,
        'license': dataset.get_license_display() or None,
        'webpage': dataset.main_webpage if dataset.main_webpage else None,
        'external_download_url': dataset.external_download_url if dataset.external_download_url else None,
        'doi': dataset.doi.replace("http://doi.org/", "") if dataset.doi else None,
        'authors': authors if len(authors) > 0 else None,
        'wam_icon': _decide_warm_icon(dataset) or None,
        'projects': projects,
    }


############################################################################
# Function: _decide_warm_icon
############################################################################

def _decide_warm_icon(dataset):
    """
    This internal class choose what type of icon should be used in the template in order to warm to the user
    about the type dataset license

    :param dataset:
    :return: free: If the dataset license is free to , commercial purposes
            open: If the dataset contains a middle license with citation needed. NON-COMMERCIAL
            restricted: If the dataset has a restricted license, citation must be used.
    """

    if dataset.license in ['ne', 'pd', 'ap', 'mit', 'cc']:
        # Green square
        return "fa-green fa-check-square"
    elif dataset.license in ['gpl', 'odc', 'ogl']:
        # Yellow exclamation
        return "fa-yellow fa-exclamation-triangle"
    else:
        # Red circle error
        return "fa-red fa-times-circle"
