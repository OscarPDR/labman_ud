# -*- coding: utf-8 -*-

from entities.projects.models import Project

import logging
logger = logging.getLogger(__name__)


###     check_project_dates()
####################################################################################################

def check_project_dates():

    logger.info(u'Check all start/end dates for projects')
    logger.info(u'')

    for project in Project.objects.filter(start_month=''):
        logger.info(u'Project <%s> has no starting month, setting default to 1 (Jan)' % project.slug)

        project.start_month = 1
        project.save()

    for project in Project.objects.filter(end_month=''):
        logger.info(u'Project <%s> has no ending month, setting default to 12 (Dec)' % project.slug)

        project.end_month = 12
        project.save()
