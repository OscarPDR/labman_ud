# -*- encoding: utf-8 -*-


from rdflib import Literal

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *

# print graph.serialize(format='turtle')
# print graph.serialize(format='n3')
# print graph.serialize(format='xml')


###########################################################################
# Model: Country
###########################################################################

def save_country_as_rdf(country):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_country_from_slug(country.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, PLACES.Country))
    graph.add((resource_uri, RDFS.label, Literal(country.full_name)))

    # Full name is required
    graph.add((resource_uri, DC.title, Literal(country.full_name)))

    # Short name is always present
    graph.add((resource_uri, DC.identifier, Literal(country.short_name)))

    insert_by_post(graph)


def delete_country_rdf(country):
    resource_uri = resource_uri_for_country_from_slug(country.slug)

    delete_resource(resource_uri)


###########################################################################
# Model: GeographicalScope
###########################################################################

def save_geographical_scope_as_rdf(geographical_scope):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_geographical_scope_from_slug(geographical_scope.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRCFE.GeographicalScope))
    graph.add((resource_uri, RDFS.label, Literal(geographical_scope.name)))

    # Name is required
    graph.add((resource_uri, DC.title, Literal(geographical_scope.name)))

    # Description is optional
    graph.add((resource_uri, DC.description, Literal(geographical_scope.description)))

    insert_by_post(graph)


def delete_geographical_scope_rdf(geographical_scope):
    resource_uri = resource_uri_for_geographical_scope_from_slug(geographical_scope.slug)

    delete_resource(resource_uri)


###########################################################################
# Model: Tag
###########################################################################

def save_tag_as_rdf(tag):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_tag_from_slug(tag.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, MUTO.Tag))
    graph.add((resource_uri, RDFS.label, Literal(tag.name)))

    # Name is required
    graph.add((resource_uri, MUTO.tagLabel, Literal(tag.name)))

    # Sub Tag Of is optional
    # graph.add((resource_uri, ???, Literal(tag.sub_tag_of)))

    insert_by_post(graph)


def delete_tag_rdf(tag):
    resource_uri = resource_uri_for_tag_from_slug(tag.slug)

    delete_resource(resource_uri)
