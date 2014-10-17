from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from entities.persons.models import Person

import difflib
import itertools


# Create your views here.


def check_names_similarity(request, threshold_ratio=50):
    threshold_ratio = float(threshold_ratio) / 100

    name_list = []
    similarities = []

    persons = Person.objects.all()

    for person in persons:
        name_list.append(person.full_name)

    for test_name, testing_name in itertools.combinations(name_list, 2):
        ratio = difflib.SequenceMatcher(None, test_name, testing_name).ratio()

        if (ratio > threshold_ratio):
            test_person = Person.objects.get(full_name=test_name)
            testing_person = Person.objects.get(full_name=testing_name)

            similarities.append({
                'test_person': test_person,
                'testing_person': testing_person,
                'ratio': ratio,
            })

    return_dict = {
        'similarities': similarities,
        'threshold_ratio': threshold_ratio,
    }

    return render(request, 'management/index.html', return_dict)


def assign_alias(request, person_id, alias_id):
    print 'blahblah'

    return HttpResponseRedirect(reverse('check_names_similarity_default'))
