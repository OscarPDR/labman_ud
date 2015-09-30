# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from maintenance_tasks.publications.synchronize_zotero import synchronize_zotero


class Command(BaseCommand):

    help = u"Synchonises the actual publication database with zotero's last version"

    def handle(self, *args, **options):
        synchronize_zotero()
