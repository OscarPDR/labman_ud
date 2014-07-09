# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.projects.check_non_filled_dates import check_non_filled_dates


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Checks for projects which start/end dates is not completed'

    def handle_noargs(self, **options):
        check_non_filled_dates()
