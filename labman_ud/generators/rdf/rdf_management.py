# -*- encoding: utf-8 -*-


import urllib
import urllib2
from rdflib import URIRef

from django.conf import settings


def resource_uri_for_person_from_slug(slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'people', slug))


def insert_by_post(graph):
    triples = ''

    for s, p, o in graph.triples((None, None, None)):
        triple = "%s %s %s . " % (s.n3(), p.n3(), o.n3())
        triples += triple

    query = 'INSERT IN GRAPH <%s> { %s }' % (getattr(settings, 'GRAPH_BASE_URL', None), triples.encode('utf-8'))

    data = urllib.urlencode({'query': query})
    request = urllib2.Request(getattr(settings, 'SPARQL_ENDPOINT_URL', None), data)
    urllib2.urlopen(request)


def delete_resource(resource_uri):
    query = """
        WITH <%s>
        DELETE { <%s> ?p ?o }
        WHERE {
            <%s> ?p ?o .
        }""" % (getattr(settings, 'GRAPH_BASE_URL', None), resource_uri, resource_uri)

    data = urllib.urlencode({'query': query})
    request = urllib2.Request(getattr(settings, 'SPARQL_ENDPOINT_URL', None), data)
    urllib2.urlopen(request)


def update_resource_uri(old_resource_uri, new_resource_uri):
    query = """
        WITH <%s>
        DELETE { ?s ?p <%s> }
        INSERT { ?s ?p <%s> }
        WHERE {
            ?s ?p <%s> .
        }""" % (getattr(settings, 'GRAPH_BASE_URL', None), old_resource_uri, new_resource_uri, old_resource_uri)

    data = urllib.urlencode({'query': query})
    request = urllib2.Request(getattr(settings, 'SPARQL_ENDPOINT_URL', None), data)
    urllib2.urlopen(request)
