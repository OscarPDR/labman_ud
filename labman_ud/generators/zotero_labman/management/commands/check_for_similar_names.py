# encoding: utf-8

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import check_for_similar_names


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Checks for similar researcher full names to include as aliases'

    def handle_noargs(self, **options):
        check_for_similar_names(0.75)
