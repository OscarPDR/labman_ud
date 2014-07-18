# -*- coding: utf-8 -*-


from generators.rdf.rdf_management import empty_graph

from entities.events.models import *
from entities.funding_programs.models import *
from entities.news.models import *
from entities.organizations.models import *
from entities.persons.models import *
from entities.projects.models import *
from entities.publications.models import *
from entities.utils.models import *


###########################################################################
# def: republish_all_data_as_rdf()
###########################################################################

def republish_all_data_as_rdf():
    print '#' * 80
    print 'Re-publishing all the information as Linked Open Data...'
    print '#' * 80

    print '\tCleaning SPARQL graph...'
    empty_graph()
    print '\t\Graph is now empty'

    print
    print 'Starting process... this may take a while'
    print

    print '\tRe-publishing organizations module'
    for organization in Organization.objects.all():
        try:
            organization.save()
        except:
            print 'Error while publishing: %s' % organization.full_name
    print '\t\tModule re-published'
    print

    print '\tRe-publishing persons module'
    for person in Person.objects.all():
        try:
            person.save()
        except:
            print 'Error while publishing: %s' % person.full_name
    print '\t\tModule re-published'
    print

    print '\tRe-publishing books'
    for book in Book.objects.all():
        try:
            book.save()
        except:
            print 'Error while publishing: %s' % book.title
    print '\t\Books re-published'
    print
