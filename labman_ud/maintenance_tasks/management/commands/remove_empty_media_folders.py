# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from maintenance_tasks.general.remove_empty_media_folders import remove_empty_media_folders


class Command(BaseCommand):

    help = u"Recursively removes empty folders in the MEDIA folder"

    def handle(self, *args, **options):
        remove_empty_media_folders()
