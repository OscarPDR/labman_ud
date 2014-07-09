# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.publications.reset_publications import reset_publications


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes every publication in labman and restarts it with data from Zotero.'

    def handle_noargs(self, **options):
        reset_publications()
