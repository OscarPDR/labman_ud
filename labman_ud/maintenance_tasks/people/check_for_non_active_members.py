# -*- coding: utf-8 -*-


from entities.persons.models import Person, Job

from datetime import date


###########################################################################
# def: check_for_non_active_members()
###########################################################################

def check_for_non_active_members():
    print '#' * 80
    print 'Checking for non active members...'
    print '#' * 80

    today = date.today()

    persons = Person.objects.filter(is_active=True)

    for person in persons:
        last_job = Job.objects.filter(person_id=person.id).order_by('-end_date')[0]

        if (last_job.end_date) and (last_job.end_date < today):
            print '\t\t%s is no longer active' % person.full_name

            person.is_active = False
            person.save()

            print '\t\t%s\'s status changed to non-active' % person.full_name
