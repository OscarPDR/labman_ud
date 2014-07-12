# -*- coding: utf-8 -*-


from entities.persons.models import Person

import difflib
import itertools


###########################################################################
# def: check_names_similarity()
###########################################################################

def check_names_similarity(threshold_ratio):
    print '#' * 80
    print 'Checking for similar names...'
    print '#' * 80

    name_list = []

    persons = Person.objects.all()

    for person in persons:
        name_list.append(person.full_name)

    for test_name, testing_name in itertools.combinations(name_list, 2):
        ratio = difflib.SequenceMatcher(None, test_name, testing_name).ratio()

        if (ratio > threshold_ratio):
            comparison_string = test_name.ljust(30) + '<=>' + testing_name.rjust(30)
            print '%f\t%s' % (ratio, comparison_string)
