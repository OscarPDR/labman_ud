# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from maintenance_tasks.projects.check_project_dates import check_project_dates


class Command(BaseCommand):

    help = u"Checks for projects which start/end dates is not completed"

    def handle(self, *args, **options):
        check_project_dates()
