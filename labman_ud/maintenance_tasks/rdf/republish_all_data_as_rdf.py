# -*- coding: utf-8 -*-


from generators.rdf.rdf_management import empty_graph

from entities.events.models import *
from entities.organizations.models import *
from entities.persons.models import *
from entities.projects.models import *
from entities.publications.models import *

import logging
logger = logging.getLogger(__name__)


###     republish_all_data_as_rdf()
#####################################################################################################

def republish_all_data_as_rdf():

    logger.info(u'')
    logger.info(u'Request to re-publish all data as Linked Open Data')

    logger.info(u'\tCleaning SPARQL graph')
    empty_graph()
    logger.info(u'\tGraph empty')

    logger.info(u'')

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

    logger.info(u'Re-publishing all data in <%s> module' % module_name)

    for item in module_item_set:
        try:
            item.save()

        except:
            failed_items.append(item)
            logger.warn(u'\tError while publishing item with ID (%d): %s' % (item.id, item))

    logger.debug(u'First publishing loop finished')

    if len(failed_items) > 0:
        for item in failed_items:
            logger.info(u'\tTrying to re-publish item with ID (%d): %s' % (item.id, item))

            try:
                logger.debug(u'\t\tSuccess')
                item.save()

            except:
                logger.warn(u'\t\tFailed again')

    logger.info(u'<%s> module re-published' % module_name)
