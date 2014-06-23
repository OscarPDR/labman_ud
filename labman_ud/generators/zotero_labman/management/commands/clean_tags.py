# -*- coding: utf-8 -*-
"""
Created on Mon Jun 23 14:44:45 2014

@author: aitor
"""

from django.core.management.base import NoArgsCommand

from generators.zotero_labman.utils import clean_tags


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Dissambiguates tags'

    def handle_noargs(self, **options):
        clean_tags()
