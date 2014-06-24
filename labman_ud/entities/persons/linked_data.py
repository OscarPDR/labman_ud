# -*- encoding: utf-8 -*-


from rdflib import Graph, ConjunctiveGraph
from rdflib.namespace import FOAF
from rdflib import URIRef, Literal

from django.conf import settings

from generators.rdf.rdf_management import insert_by_post


def person_to_rdf(person):
    graph = Graph()

    resource_uri = URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'people', person.slug))

    graph.add((resource_uri, FOAF.first_name, Literal(person.first_name)))

    print graph.serialize(format='turtle')

    insert_by_post(graph)
