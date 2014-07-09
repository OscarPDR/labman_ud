# -*- coding: utf-8 -*-

from entities.person.models import Person, Job
from entities.organization.models import Organization


###########################################################################
# def: remove_unrelated_people()
###########################################################################

def remove_unrelated_people():
    print '#' * 80
    print 'Checking for unrelated people to remove...'
    print '#' * 80

    unused_person_ids = set()
    organization_slugs = ['morelab', 'deustotech-internet', 'deustotech-telecom']

    all_persons = Person.objects.all()
    own_organizations = Organization.objects.filter(slug__in=organization_slugs)

    for person in all_persons:
        publications = person.publications.all()
        projects = person.projects.all()

        if (len(publications) == 0) and (len(projects) == 0):
            unused_person_ids.add(person.id)

    unused_persons = Person.objects.filter(id__in=unused_person_ids, is_active=False)

    persons_to_remove = set()

    removed_objects = 0

    for person in unused_persons:
        jobs = Job.objects.filter(person=person, organization__in=own_organizations)

        if len(jobs) == 0:
            removed_objects += 1
            persons_to_remove.add(person)

            print '\tPerson to be deleted: %s' % person.full_name
            person.delete()

    print 'Removed %d items' % removed_objects
