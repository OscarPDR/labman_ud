# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.general.clean_tags import clean_tags


class Command(NoArgsCommand):
    can_import_settings = True

    help = ''

    def handle_noargs(self, **options):
        clean_tags()
