# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from maintenance_tasks.people.check_people_redundancy import check_people_redundancy


class Command(BaseCommand):

    help = u"Checks if any publication author is redundant as he/she is using one of his/her nicknames"

    def handle(self, *args, **options):
        check_people_redundancy()
