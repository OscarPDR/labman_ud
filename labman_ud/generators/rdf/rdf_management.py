# -*- encoding: utf-8 -*-


import urllib
import urllib2

from django.conf import settings


def insert_by_post(graph):
    triples = ''

    for s, p, o in graph.triples((None, None, None)):
        triple = "%s %s %s . " % (s.n3(), p.n3(), o.n3())
        triples += triple

    query = 'INSERT IN GRAPH <%s> { %s }' % (getattr(settings, 'GRAPH_BASE_URL', None), triples.encode('utf-8'))

    data = urllib.urlencode({'query': query})
    request = urllib2.Request(getattr(settings, 'SPARQL_ENDPOINT_URL', None), data)
    urllib2.urlopen(request)
