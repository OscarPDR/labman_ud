#encoding: utf-8 

from django.core.management.base import NoArgsCommand
from django.core.management import call_command

from labman_ud import settings
from generators.zotero_labman.models import ZoteroLog
from entities.publications.models import Publication
from entities.projects.models import RelatedPublication

from datetime import datetime
from django.utils.timezone import utc

from generators.zotero_labman.utils import delete_publication

import os

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes every publication in labman (saving only relations between publications and projects) and restarts it with data from Zotero.'

    def handle_noargs(self, **options):
        print "[RESET_PUBS] Deleting every publication in DB..."

        backup_dataset = []

        for pub in Publication.objects.all():
            backup_data = delete_publication(pub)
            if backup_data:
                backup_dataset.append(backup_data)

        # Generate a log specifying a Zotero library version equal to 0, with the aim of re-syncing all publications
        zotlog = ZoteroLog(zotero_key='-RESYNC-', updated=datetime.utcnow().replace(tzinfo=utc), version=0, observations='')
        zotlog.save()

        # Sync again the library with data from Zotero (calling the sync_zotero command)
        print "\n[RESET_PUBS] Re-syncing with Zotero..."
        call_command('sync_zotero')
