# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from maintenance_tasks.publications.reset_publications import reset_publications


class Command(BaseCommand):

    help = u"Removes every publication in labman and resets it with data from Zotero"

    def handle(self, *args, **options):
        reset_publications()
