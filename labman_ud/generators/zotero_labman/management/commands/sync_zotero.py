#encoding: utf-8 

from django.core.management.base import NoArgsCommand
from generators.zotero_labman.models import ZoteroLog

from generators.zotero_labman.utils import get_zotero_variables, parse_last_items, sync_deleted_items

import requests
import operator

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Synchronizes Labman\'s publications DB with data from your Zotero library.'

    def handle_noargs(self, **options):
        try:
            last_version_db = ZoteroLog.objects.all().order_by('-created')[0].version
        except:
            last_version_db = 0

        # Get last version in Zotero repository
        api_key, library_id, library_type, api_limit = get_zotero_variables()

        r = requests.get('https://api.zotero.org/'+  library_type + 's/'+ library_id + '/items?format=versions&key=' + api_key)
        last_version_zotero = max(r.json().items(), key=operator.itemgetter(1))[1]

        # Get unsynchronized items and remove those which have been removed in Zotero
        parse_last_items(last_version_zotero, last_version_db)
        if last_version_db != 0:
            sync_deleted_items(last_version_zotero, last_version_db)


    

    

