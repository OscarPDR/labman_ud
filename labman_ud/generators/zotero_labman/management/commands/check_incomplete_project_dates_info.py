# encoding: utf-8

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import check_incomplete_project_dates_info


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Checks for projects which start/end dates is not completed'

    def handle_noargs(self, **options):
        check_incomplete_project_dates_info()
