# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand
from django.conf import settings

from maintenance_tasks.general.remove_empty_folders import remove_empty_folders


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Recursively removes empty folders in the MEDIA folder'

    def handle_noargs(self, **options):
        remove_empty_folders(getattr(settings, 'MEDIA_ROOT', None), True)
