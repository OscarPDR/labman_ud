# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.people.check_author_redundancy_through_nicks import check_author_redundancy_through_nicks
from maintenance_tasks.people.check_for_non_active_members import check_for_non_active_members
from maintenance_tasks.people.check_names_similarity import check_names_similarity


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Maintenance tasks related to people'

    def handle_noargs(self, **options):
        # Checks if any publication author is redundant as he/she is using one of his/her nicknames
        check_author_redundancy_through_nicks()

        # Checks name similarity above the provided threshold
        check_names_similarity(0.75)

        # Checks for members which are no longer active
        check_for_non_active_members()
