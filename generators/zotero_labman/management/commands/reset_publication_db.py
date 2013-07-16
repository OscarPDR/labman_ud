#encoding: utf-8 

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.models import ZoteroLog
from entities.publications.models import Publication, PublicationType, PublicationAuthor, PublicationTag

from django.core.management import call_command

from datetime import datetime

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes every publication in labman (saving only relations between publications and projects) and restarts it with data from Zotero.'

    def handle_noargs(self, **options):
        Publication.objects.all().delete()
        zotlog = ZoteroLog(zotero_key='RESYNC', updated=datetime.now(), version=0, observations='')

        # Sync again the library with data from Zotero (calling the sync_zotero command)
        call_command('sync_zotero')