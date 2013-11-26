# encoding: utf-8

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import remove_unrelated_tags


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes tags not related to any other model instance'

    def handle_noargs(self, **options):
        remove_unrelated_tags()
