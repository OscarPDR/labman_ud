# -*- encoding: utf-8 -*-


from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *


###########################################################################
# Model: Event
###########################################################################

def save_event_as_rdf(event):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_event_from_slug(event.slug)

    # Define type and label of resource
    if event.event_type == 'Academic event':
        graph.add((resource_uri, RDF.type, SWRC.Conference))
    elif event.event_type == 'Generic event':
        graph.add((resource_uri, RDF.type, SWRC.Event))
    elif event.event_type == 'Hackathon':
        graph.add((resource_uri, RDF.type, SWRCFE.Hackathon))
    elif event.event_type == 'Project meeting':
        graph.add((resource_uri, RDF.type, SWRC.ProjectMeeting))

    graph.add((resource_uri, RDFS.label, Literal(event.full_name)))

    # Full name is required
    graph.add((resource_uri, DC.title, Literal(event.full_name)))

    # Short name is always present
    graph.add((resource_uri, DC.identifier, Literal(event.short_name)))

    # Location is optional
    if event.location:
        graph.add((resource_uri, SWRCFE.eventLocation, Literal(event.location)))

    # host city
    # TODO: Publish city as RDF

    # host country
    # TODO: Publish country as RDF

    # Start date is optional
    if event.start_date:
        graph.add((resource_uri, SWRCFE.eventStartDate, Literal(event.start_date, datatype=XSD.date)))

    # End date is optional
    if event.end_date:
        graph.add((resource_uri, SWRCFE.eventEndDate, Literal(event.end_date, datatype=XSD.date)))

    # Year is required
    graph.add((resource_uri, SWRCFE.year, Literal(event.year, datatype=XSD.gYear)))

    # Homepage is optional
    if event.homepage:
        graph.add((resource_uri, FOAF.homepage, URIRef(event.homepage)))

    # Description is optional
    if event.description:
        graph.add((resource_uri, DC.description, Literal(event.description)))

    # Logo is optional
    if event.logo:
        event_logo_url = '%s%s' % (getattr(settings, 'BASE_URL', None), event.logo.url)
        graph.add((resource_uri, FOAF.depiction, Literal(event_logo_url)))

    # Proceedings is optional
    if event.proceedings:
        graph.add((resource_uri, SWRCFE.hasProceedings, resource_uri_for_event_from_slug(event.proceedings.slug)))

    if len(event.personrelatedtoevent_set.all()) > 0:
        for person_related_to_event in event.personrelatedtoevent_set.all():
            graph.add((resource_uri, SWRCFE.hasParticipant, resource_uri_for_person_from_slug(person_related_to_event.person.slug)))

    insert_by_post(graph)


def update_event_object_triples(old_slug, new_slug):
    old_resource_uri = resource_uri_for_event_from_slug(old_slug)
    new_resource_uri = resource_uri_for_event_from_slug(new_slug)

    update_resource_uri(old_resource_uri, new_resource_uri)


def delete_event_rdf(event):
    resource_uri = resource_uri_for_event_from_slug(event.slug)

    delete_resource(resource_uri)


###########################################################################
# Model: EventSeeAlso
###########################################################################

def save_event_see_also_as_rdf(event_see_also):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_event_from_slug(event_see_also.event.slug)

    graph.add((resource_uri, RDFS.seeAlso, URIRef(event_see_also.see_also)))

    insert_by_post(graph)


def delete_event_see_also_rdf(event_see_also):
    resource_uri = resource_uri_for_event_from_slug(event_see_also.event.slug)

    delete_resources_with_predicate(resource_uri, RDFS.seeAlso)


###########################################################################
# Model: PersonRelatedToEvent
###########################################################################

def save_person_related_to_event_as_rdf(person_related_to_event):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_event_from_slug(person_related_to_event.event.slug)

    graph.add((resource_uri, SWRCFE.hasParticipant, resource_uri_for_person_from_slug(person_related_to_event.person.slug)))

    insert_by_post(graph)


def delete_person_related_to_event_rdf(person_related_to_event):
    resource_uri = resource_uri_for_event_from_slug(person_related_to_event.event.slug)

    delete_resources_with_predicate(resource_uri, SWRCFE.hasParticipant)
