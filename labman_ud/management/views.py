from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.conf import settings

from entities.persons.models import Person, Nickname
from .models import IgnoredSimilarNames

from maintenance_tasks.people.check_author_redundancy_through_nicks import *

import difflib
import itertools
from operator import itemgetter

# Create your views here.

DEFAULT_THRESHOLD_RATIO = getattr(settings, 'DEFAULT_THRESHOLD_RATIO', 60)


def index(request):

    return_dict = {}

    return render(request, 'management/index.html', return_dict)


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


def reset_ignored_relationships(request, threshold_ratio):

    for item in IgnoredSimilarNames.objects.all():
        item.delete()

    if threshold_ratio == DEFAULT_THRESHOLD_RATIO:
        return HttpResponseRedirect(reverse('check_names_similarity_default'))

    else:
        return HttpResponseRedirect(reverse('check_names_similarity', args=[threshold_ratio]))
