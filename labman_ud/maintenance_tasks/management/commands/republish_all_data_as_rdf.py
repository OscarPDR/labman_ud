# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from maintenance_tasks.rdf.republish_all_data_as_rdf import republish_all_data_as_rdf


class Command(BaseCommand):

    help = u"Empties previously existing SPARQL graphs (if any) and re-publishes everything as RDF"

    def handle(self, *args, **options):
        republish_all_data_as_rdf()
