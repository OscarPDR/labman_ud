# encoding: utf-8

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import check_for_non_active_members


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Checks for members which are no longer active'

    def handle_noargs(self, **options):
        check_for_non_active_members()
