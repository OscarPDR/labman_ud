# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.publications.parse_publication import parse_publication


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Test'

    def handle_noargs(self, **options):
        parse_publication()
