# -*- coding: utf-8 -*-

from django.core.management.base import NoArgsCommand

from maintenance_tasks.rdf.republish_all_data_as_rdf import republish_all_data_as_rdf


class Command(NoArgsCommand):
    can_import_settings = True

    help = 'Empties previously existing SPARQL graphs (if any) and re-publishes everything as RDF'

    def handle_noargs(self, **options):
        republish_all_data_as_rdf()
