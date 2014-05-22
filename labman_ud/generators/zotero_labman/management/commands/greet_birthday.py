# encoding: utf-8

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import greet_birthday


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Checks if today is some members birthday'

    def handle_noargs(self, **options):
        greet_birthday()
