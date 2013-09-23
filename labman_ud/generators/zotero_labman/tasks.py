from celery.task.schedules import crontab
from celery.task import periodic_task

from django.core.management import call_command
from django.conf import settings

from generators.zotero_labman.utils import logger

import traceback


@periodic_task(
    run_every=getattr(settings, 'ZOTERO_CRONTAB', crontab(hour='*/1'))
)
def sync_zotero():
    try:
        call_command('sync_zotero')
    except:
        logger.error(traceback.format_exc())
        # Send email?
        raise
