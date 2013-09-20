#encoding: utf-8 

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.models import ZoteroLog
from entities.publications.models import Publication

from datetime import datetime
from django.utils.timezone import utc

from generators.zotero_labman.utils import delete_publication, get_last_zotero_version, parse_last_items, logger

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes every publication in labman (saving only relations between publications and projects) and restarts it with data from Zotero.'

    def handle_noargs(self, **options):
        logger.info('Deleting every publication in DB...')

        backup_dataset = []

        for pub in Publication.objects.all():
            backup_data = delete_publication(pub)
            if backup_data:
                backup_dataset.append(backup_data)

        # Generate a log specifying a Zotero library version equal to 0, with the aim of re-syncing all publications
        zotlog = ZoteroLog(zotero_key='-RESYNC-', updated=datetime.utcnow().replace(tzinfo=utc), version=0, observations='')
        zotlog.save()

        # Sync again the library with data from Zotero
        logger.info('Re-syncing with Zotero...')
        last_version_zotero = get_last_zotero_version()
        parse_last_items(last_version_zotero, 0)
