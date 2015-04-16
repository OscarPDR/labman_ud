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
    print

    print 'Cleaning SPARQL graph...'
    empty_graph()
    print 'Graph is now empty'

    _publish_module('Organization', Organization.objects.all())
    _publish_module('Person', Person.objects.all())
    _publish_module('Event', Event.objects.all())
    _publish_module('Project', Project.objects.all())

    print '\tRe-publishing publications module'
    for publication in Publication.objects.all():

        try:
            if publication.child_type == 'Book':
                book = Book.objects.get(slug=publication.slug)
                book.save()

            elif publication.child_type == 'BookSection':
                book_section = BookSection.objects.get(slug=publication.slug)
                book_section.save()

            elif publication.child_type == 'ConferencePaper':
                conference_paper = ConferencePaper.objects.get(slug=publication.slug)
                conference_paper.save()

            elif publication.child_type == 'Proceedings':
                proceedings = Proceedings.objects.get(slug=publication.slug)
                proceedings.save()

            if publication.child_type == 'JournalArticle':
                journal_article = JournalArticle.objects.get(slug=publication.slug)
                journal_article.save()

            if publication.child_type == 'Journal':
                journal = Journal.objects.get(slug=publication.slug)
                journal.save()

            if publication.child_type == 'MagazineArticle':
                magazine_article = MagazineArticle.objects.get(slug=publication.slug)
                magazine_article.save()

            if publication.child_type == 'Magazine':
                magazine = Magazine.objects.get(slug=publication.slug)
                magazine.save()

        except:
            print 'Error while publishing: %s' % publication.title
    print '\t\Module re-published'
    print


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
            print '\tError while publishing: (%d) %s' % (item.id, item)

    print 'First loop finished'
    print

    if len(failed_items) > 0:
        for item in failed_items:
            print u'\tTrying to re-publish: (%d) %s' % (item.id, item)

            try:
                print '\t\tSuccess'
                item.save()

            except:
                print '\t\tFailed again'

    print
    print '-' * 50
    print
