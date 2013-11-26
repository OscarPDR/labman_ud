#encoding: utf-8 

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import check_what_is_missing, get_last_zotero_version, logger
class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes every publication in labman (saving only relations between publications and projects) and restarts it with data from Zotero.'

    def handle_noargs(self, **options):
        logger.info('Checking if any publication hasn\'t been parsed by sync_zotero...')

        check_what_is_missing(get_last_zotero_version())