# -*- encoding: utf-8 -*-


import urllib
import urllib2

from rdflib import Graph
from rdflib.namespace import Namespace, FOAF, DC, XSD, RDF, RDFS

from django.conf import settings

GEONAMES = Namespace('http://www.geonames.org/ontology#')
MUTO = Namespace('http://purl.org/muto/core#')
PLACES = Namespace('http://purl.org/ontology/places#')
SWRCFE = Namespace('http://www.morelab.deusto.es/ontologies/swrcfe#')
DCTERMS = Namespace('http://purl.org/dc/terms/')


def create_namespaced_graph():
    graph = Graph()

    graph.bind('dc', DC)
    graph.bind('dcterms', DCTERMS)
    graph.bind('foaf', FOAF)
    graph.bind('geonames', GEONAMES)
    graph.bind('muto', MUTO)
    graph.bind('places', PLACES)
    graph.bind('rdf', RDF)
    graph.bind('rdfs', RDFS)
    graph.bind('swrcfe', SWRCFE)
    graph.bind('xsd', XSD)

    return graph


def _perform_request(query):
    data = urllib.urlencode({'query': query})
    request = urllib2.Request(getattr(settings, 'SPARQL_ENDPOINT_URL', None), data)
    urllib2.urlopen(request)


def insert_by_post(graph):
    triples = ''

    for s, p, o in graph.triples((None, None, None)):
        triple = "%s %s %s . " % (s.n3(), p.n3(), o.n3())
        triples += triple

    query = 'INSERT IN GRAPH <%s> { %s }' % (getattr(settings, 'GRAPH_BASE_URL', None), triples.encode('utf-8'))

    _perform_request(query)


def delete_resource(resource_uri):
    query = """
        WITH <%s>
        DELETE { <%s> ?p ?o . }
        WHERE {
            <%s> ?p ?o .
        }""" % (getattr(settings, 'GRAPH_BASE_URL', None), resource_uri, resource_uri)

    _perform_request(query)


def delete_resources_with_predicate(resource_uri, predicate):
    query = """
        WITH <%s>
        DELETE { <%s> <%s> ?o . }
        WHERE {
            <%s> <%s> ?o .
        }""" % (getattr(settings, 'GRAPH_BASE_URL', None), resource_uri, predicate, resource_uri, predicate)

    _perform_request(query)


def update_resource_uri(old_resource_uri, new_resource_uri):
    query = """
        WITH <%s>
        DELETE { ?s ?p <%s> . }
        INSERT { ?s ?p <%s>  .}
        WHERE { ?s ?p <%s> .}
    """ % (getattr(settings, 'GRAPH_BASE_URL', None), old_resource_uri, new_resource_uri, old_resource_uri)

    _perform_request(query)


def empty_graph():
    query = """
        WITH <%s>
        DELETE { ?s ?p ?o . }
        WHERE { ?s ?p ?o . }
    """ % getattr(settings, 'GRAPH_BASE_URL', None)

    _perform_request(query)
