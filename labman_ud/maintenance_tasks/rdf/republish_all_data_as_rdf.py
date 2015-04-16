# -*- coding: utf-8 -*-


from generators.rdf.rdf_management import empty_graph

from entities.events.models import *
from entities.organizations.models import *
from entities.persons.models import *
from entities.projects.models import *
from entities.publications.models import *


###     republish_all_data_as_rdf()
#####################################################################################################

def republish_all_data_as_rdf():

    print
    print '#' * 80
    print 'Re-publishing all the information as Linked Open Data...'
    print '#' * 80
    print

    print 'Cleaning SPARQL graph...'
    empty_graph()
    print 'Graph is now empty'
    print

    _publish_module('Event', Event.objects.all())
    _publish_module('Organization', Organization.objects.all())
    _publish_module('Person', Person.objects.all())
    _publish_module('Project', Project.objects.all())

    _publish_module('Book', Book.objects.all())
    _publish_module('BookSection', BookSection.objects.all())
    _publish_module('Proceedings', Proceedings.objects.all())
    _publish_module('ConferencePaper', ConferencePaper.objects.all())
    _publish_module('Journal', Journal.objects.all())
    _publish_module('JournalArticle', JournalArticle.objects.all())
    _publish_module('Magazine', Magazine.objects.all())
    _publish_module('MagazineArticle', MagazineArticle.objects.all())


###     _publish_module(module_name, module_item_set)
####################################################################################################

def _publish_module(module_name, module_item_set):

    failed_items = []

    print "Re-publishing '%s' module" % module_name

    for item in module_item_set:
        try:
            item.save()

        except:
            failed_items.append(item)
            print '\tError while publishing item with ID (%d): %s' % (item.id, item)

    print 'First loop finished'

    if len(failed_items) > 0:
        print

        for item in failed_items:
            print u'\tTrying to re-publish item with ID (%d): %s' % (item.id, item)

            try:
                print '\t\tSuccess'
                item.save()

            except:
                print '\t\tFailed again'

    print
    print '-' * 50
    print
