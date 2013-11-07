#encoding: utf-8 

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import correct_nicks

class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes duplicate authors when nicknames coincide'

    def handle_noargs(self, **options):
        correct_nicks()
