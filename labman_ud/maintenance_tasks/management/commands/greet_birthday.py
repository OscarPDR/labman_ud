# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.people.greet_birthday import greet_birthday


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Checks if today is any member\'s birthday, if so, it sends an email greeting him/her'

    def handle_noargs(self, **options):
        greet_birthday()
