# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.publications.synchronize_zotero import synchronize_zotero


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes every publication in labman and resets it with data from Zotero.'

    def handle_noargs(self, **options):
        synchronize_zotero()
