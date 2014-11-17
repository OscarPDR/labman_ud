
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render

from entities.persons.models import Person, Nickname

from .models import IgnoredSimilarNames
from .forms import *

from maintenance_tasks.people.check_author_redundancy_through_nicks import *
from extractors.zotero.zotero_extractor import *

import difflib
import itertools
from operator import itemgetter


# Create your views here.


DEFAULT_THRESHOLD_RATIO = getattr(settings, 'DEFAULT_THRESHOLD_RATIO', 60)


####################################################################################################
###     View: index()
####################################################################################################

@login_required
def index(request):

    return_dict = {}

    return render(request, 'management/index.html', return_dict)


####################################################################################################
###     View: check_names_similarity(threshold_ratio)
####################################################################################################

@login_required
def check_names_similarity(request, threshold_ratio=DEFAULT_THRESHOLD_RATIO):
    normalized_threshold_ratio = float(threshold_ratio) / 100

    name_list = []
    similarities = []

    persons = Person.objects.all()

    for person in persons:
        name_list.append(person.full_name)

    for test_name, testing_name in itertools.combinations(name_list, 2):
        ratio = difflib.SequenceMatcher(None, test_name, testing_name).ratio()

        if (ratio > normalized_threshold_ratio):
            test_person = Person.objects.get(full_name=test_name)
            testing_person = Person.objects.get(full_name=testing_name)

            try:
                check_1 = IgnoredSimilarNames.objects.get(test_person=test_person, testing_person=testing_person)
            except:
                check_1 = None

            try:
                check_2 = IgnoredSimilarNames.objects.get(test_person=testing_person, testing_person=test_person)
            except:
                check_2 = None

            if not (check_1 or check_2):
                similarities.append({
                    'test_person': test_person,
                    'testing_person': testing_person,
                    'ratio': ratio,
                })

    sorted_similarities = sorted(similarities, key=itemgetter('ratio'), reverse=True)

    return_dict = {
        'similarities': sorted_similarities,
        'threshold_ratio': threshold_ratio,
    }

    return render(request, 'management/name_similarities.html', return_dict)


####################################################################################################
###     View: assign_alias(person_id, alias_id, threshold_ratio)
####################################################################################################

@login_required
def assign_alias(request, person_id, alias_id, threshold_ratio):
    valid_person = Person.objects.get(id=person_id)
    alias_person = Person.objects.get(id=alias_id)

    nickname = Nickname(
        person=valid_person,
        nickname=alias_person.full_name,
    )

    nickname.save()

    check_author_redundancy_through_nicks(valid_person)

    if threshold_ratio == DEFAULT_THRESHOLD_RATIO:
        return HttpResponseRedirect(reverse('check_names_similarity_default'))

    else:
        return HttpResponseRedirect(reverse('check_names_similarity', args=[threshold_ratio]))


####################################################################################################
###     View: ignore_relationship(test_person_id, testing_person_id, threshold_ratio)
####################################################################################################

@login_required
def ignore_relationship(request, test_person_id, testing_person_id, threshold_ratio):
    ignored_similar_names = IgnoredSimilarNames(
        test_person=Person.objects.get(id=test_person_id),
        testing_person=Person.objects.get(id=testing_person_id),
    )

    ignored_similar_names.save()

    if threshold_ratio == DEFAULT_THRESHOLD_RATIO:
        return HttpResponseRedirect(reverse('check_names_similarity_default'))

    else:
        return HttpResponseRedirect(reverse('check_names_similarity', args=[threshold_ratio]))


####################################################################################################
###     View: reset_ignored_relationships(threshold_ratio)
####################################################################################################

@login_required
def reset_ignored_relationships(request, threshold_ratio):

    for item in IgnoredSimilarNames.objects.all():
        item.delete()

    if threshold_ratio == DEFAULT_THRESHOLD_RATIO:
        return HttpResponseRedirect(reverse('check_names_similarity_default'))

    else:
        return HttpResponseRedirect(reverse('check_names_similarity', args=[threshold_ratio]))


####################################################################################################
###     View: manage_tags()
####################################################################################################

@login_required
def manage_tags(request):
    tags = Tag.objects.all().order_by('name')

    return_dict = {
        'tags': tags,
    }

    return render(request, 'management/manage_tags.html', return_dict)


####################################################################################################
###     View: rename_tag(tag_id)
####################################################################################################

@login_required
def rename_tag(request, tag_id):
    tag_to_be_renamed = Tag.objects.get(id=tag_id)

    news_tags = NewsTag.objects.filter(tag=tag_to_be_renamed)
    assigned_person_tags = AssignedPersonTag.objects.filter(tag=tag_to_be_renamed)
    project_tags = ProjectTag.objects.filter(tag=tag_to_be_renamed)
    publication_tags = PublicationTag.objects.filter(tag=tag_to_be_renamed)

    if request.method == 'POST':
        form = TagRenameForm(request.POST)

        if form.is_valid():

            tag_name = form.cleaned_data['tag_name']
            parent_tag_name = form.cleaned_data['parent_tag']

            if tag_name:
                try:
                    new_tag = Tag.objects.get(name=tag_name)

                    for news_tag in news_tags:
                        news_tag.tag = new_tag
                        news_tag.save()

                    for assigned_person_tag in assigned_person_tags:
                        assigned_person_tag.tag = new_tag
                        assigned_person_tag.save()

                    for project_tag in project_tags:
                        project_tag.tag = new_tag
                        project_tag.save()

                    for publication_tag in publication_tags:
                        publication_tag.tag = new_tag
                        publication_tag.save()

                    tag_to_be_renamed.delete()

                except:
                    tag_to_be_renamed.name = tag_name
                    tag_to_be_renamed.save()

            if parent_tag_name:
                parent_tag = Tag.objects.get(name=parent_tag_name)

                if tag_name:
                    tag_to_update = Tag.objects.get(name=tag_name)

                else:
                    tag_to_update = tag_to_be_renamed

                tag_to_update.sub_tag_of = parent_tag
                tag_to_update.save()

            return HttpResponseRedirect(reverse('manage_tags'))

    else:
        form = TagRenameForm()

    return_dict = {
        'tag_to_be_renamed': tag_to_be_renamed,
        'form': form,
        'news_tags': news_tags,
        'assigned_person_tags': assigned_person_tags,
        'project_tags': project_tags,
        'publication_tags': publication_tags,
    }

    return render(request, 'management/rename_tag.html', return_dict)


####################################################################################################
###     View: parse_publications()
####################################################################################################

@login_required
def parse_publications(request):

    if request.method == 'POST':
        form = PublicationItemForm(request.POST)

        if form.is_valid():
            item_key = form.cleaned_data['item_key']

            generate_publication_from_zotero(item_key)

        return HttpResponseRedirect(reverse('parse_publications'))

    else:
        form = PublicationItemForm()

    return_dict = {
        'form': form,
        'last_zotero_version': get_last_zotero_version(),
        'last_synchronized_zotero_version': get_last_synchronized_zotero_version(),
    }

    return render(request, 'management/parse_publications.html', return_dict)


####################################################################################################
###     View: synchronize_publications(from_version)
####################################################################################################

@login_required
def synchronize_publications(request, from_version=0):
    item_key_list = get_item_keys_since_last_synchronized_version(from_version)

    for item_key in item_key_list[:25]:
        generate_publication_from_zotero(item_key)

    return HttpResponseRedirect(reverse('parse_publications'))
