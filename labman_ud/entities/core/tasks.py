from celery.task import task
from django.conf import settings

from rdflib import Graph, ConjunctiveGraph, URIRef, Literal
from rdflib.store import Store
from rdflib.plugin import get as plugin

import re
import requests


def get_uri_for(instance):
    g = Graph()

    d2r_path = getattr(settings, 'D2R_MAPPING_PATH', None)
    g.parse(d2r_path, format='turtle')

    db_column = instance._meta.db_table

    for pat in g.query('''
        SELECT ?pattern WHERE {
            ?s a <http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#ClassMap> ;
                <http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#classDefinitionLabel> "%s" ;
                <http://www.wiwiss.fu-berlin.de/suhl/bizer/D2RQ/0.1#uriPattern> ?pattern .
        }
        ''' % db_column):
        pattern = str(pat[0])

        re_patt = re.compile('@@%s\.(?P<attr>[^@]+)@@' % db_column)

        attrs = re_patt.findall(pattern)

        if attrs:
            for attr in attrs:
                pattern = re_patt.sub(repl=str(getattr(instance, attr)), string=pattern, count=1)

    rdf_uri = getattr(settings, 'RDF_URI', None)

    g.close()

    return rdf_uri + pattern

def get_virtuoso_graph():
    virtuoso_odbc = getattr(settings, 'VIRTUOSO_ODBC', None)
    virtuoso_graph = getattr(settings, 'VIRTUOSO_GRAPH', None)

    try:
        Virtuoso = plugin("Virtuoso", Store)
        virtuoso_store = ConjunctiveGraph(store=Virtuoso(virtuoso_odbc))
        data_graph = virtuoso_store.get_context(virtuoso_graph)
    except Exception, e:
        raise Exception("Unable to connect to LTW data source: %s" % str(e))

    return data_graph

@task(ignore_result=True)
def save_rdf(instance):
    print '-'*15 + 'SAVE' + '-'*15

    data_graph = get_virtuoso_graph()

    instance_uri = get_uri_for(instance)

    params = {'query': 'SELECT DISTINCT ?p ?o WHERE { <%s> ?p ?o }' % instance_uri, 'format': 'json'}

    r = requests.get(getattr(settings, 'D2R_SPARQL_URL'), params=params)
    jsn = r.json()
    for res in jsn['results']['bindings']:
        p = URIRef(res['p']['value'])
        o = URIRef(res['o']['value']) if res['o']['type'] == 'uri' else Literal(res['o']['value'])
        try:
            if res['o']['value'] and str(o) != 'None':
                data_graph.add(( URIRef(instance_uri), p, o ))
        except:
            pass

    data_graph.close()


@task(ignore_result=True)
def delete_rdf(instance):
    print '-'*15 + 'DELETE' + '-'*15

    data_graph = get_virtuoso_graph()

    data_graph.remove((URIRef(get_uri_for(instance)), None, None))

    data_graph.close()
