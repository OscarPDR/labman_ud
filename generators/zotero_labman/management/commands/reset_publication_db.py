#encoding: utf-8 

from django.core.management.base import NoArgsCommand
from django.core.management import call_command

from labman_ud import settings
from generators.zotero_labman.models import ZoteroLog
from entities.publications.models import Publication
from entities.projects.models import RelatedPublication

from datetime import datetime
from django.utils.timezone import utc

import os

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes every publication in labman (saving only relations between publications and projects) and restarts it with data from Zotero.'

    def handle_noargs(self, **options):
        publ_proj = {}

        print "[RESET_PUBS] Deleting every publication in DB..."
        for pub in Publication.objects.all():
            # Delete PDF files
            if pub.pdf:
                try:
                    os.remove(getattr(settings, 'MEDIA_ROOT', None) + '/' + str(pub.pdf))
                except:
                    pass

            # Save relations between publications and projects
            if pub.projects.all():
                try:
                    zot_key = ZoteroLog.objects.filter(publication=pub).order_by('-created')[0].zotero_key
                    publ_proj[zot_key] = []
                    for proj in pub.projects.all():
                        publ_proj[zot_key].append(proj)
                except IndexError:
                    pass

            # Delete publication objects
            pub.delete()

        # Generate a log specifying a Zotero library version equal to 0, with the aim of re-syncing all publications
        zotlog = ZoteroLog(zotero_key='RESYNC', updated=datetime.utcnow().replace(tzinfo=utc), version=0, observations='')
        zotlog.save()

        # Sync again the library with data from Zotero (calling the sync_zotero command)
        print "\n[RESET_PUBS] Re-syncing with Zotero..."
        call_command('sync_zotero')

        print "\n\n[RESET_PUBS] Re-saving relations between publications and projects..."
        if publ_proj:
            for zot_key, projects in publ_proj.items():
                pub = ZoteroLog.objects.filter(zotero_key=zot_key).order_by('-created')[0].publication
                for proj in projects:
                    relpub = RelatedPublication(publication=pub, project=proj)
                    relpub.save()
                    print "\n[RESET_PUBS] PUB ", str(pub), " WITH PROJ: " + str(proj)
        else:
            print "\n[RESET_PUBS] No relations to sync."
