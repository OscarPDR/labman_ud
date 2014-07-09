# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.general.remove_unrelated_people import remove_unrelated_people
from maintenance_tasks.general.remove_unrelated_tags import remove_unrelated_tags


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Removes entities not related to any other model instance'

    def handle_noargs(self, **options):
        remove_unrelated_people()
        remove_unrelated_tags()
