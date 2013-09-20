from celery.task.schedules import crontab
from celery.task import periodic_task

from django.core.management import call_command
from django.conf import settings

@periodic_task(run_every=getattr(settings, 'ZOTERO_CRONTAB', crontab(hour='*/1')))
def sync_zotero():
    call_command('sync_zotero')