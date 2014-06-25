# -*- encoding: utf-8 -*-


from rdflib import Graph
from rdflib.namespace import Namespace, FOAF, RDF, RDFS, DC, XSD
from rdflib import URIRef, Literal

from django.conf import settings

from generators.rdf.rdf_management import insert_by_post, delete_resource, update_resource_uri, resource_uri_for_person_from_slug

SWRCFE = Namespace('http://www.morelab.deusto.es/ontologies/swrcfe#')


def save_person_as_rdf(person):
    print 'Saving resources of: %s' % person.slug

    graph = Graph()

    graph.bind("foaf", FOAF)
    graph.bind("dc", DC)
    graph.bind("xsd", XSD)
    graph.bind("swrcfe", SWRCFE)

    resource_uri = resource_uri_for_person_from_slug(person.slug)

    graph.add((resource_uri, RDF.type, FOAF.Person))
    graph.add((resource_uri, RDFS.label, Literal(person.full_name)))

    graph.add((resource_uri, FOAF.firstName, Literal(person.first_name)))

    surnames = person.first_surname

    if person.second_surname:
        surnames = '%s %s' % (surnames, person.second_surname)
    graph.add((resource_uri, FOAF.familyName, Literal(surnames)))

    graph.add((resource_uri, FOAF.name, Literal(person.full_name)))

    if person.birth_date:
        graph.add((resource_uri, FOAF.birthday, Literal(person.birth_date, datatype=XSD.date)))

    if person.safe_biography != '':
        graph.add((resource_uri, DC.description, Literal(person.safe_biography)))

    if person.title:
        graph.add((resource_uri, FOAF.title, Literal(person.title)))

    if person.gender:
        gender = person.gender.lower()
        graph.add((resource_uri, FOAF.gender, Literal(gender)))

    if person.personal_website:
        graph.add((resource_uri, FOAF.homepage, Literal(person.personal_website)))

    if person.email:
        graph.add((resource_uri, FOAF.mbox, Literal(person.email)))

    if person.phone_number:
        phone_number = person.phone_number

        if person.phone_extension:
            phone_number = '%s - ext: %s' % (phone_number, person.phone_extension)

        graph.add((resource_uri, FOAF.phone, Literal(phone_number)))

    graph.add((resource_uri, SWRCFE.isMember, Literal(person.is_active)))

    if person.profile_picture:
        profile_picture_url = '%s%s' % (getattr(settings, 'BASE_URL', None), person.profile_picture.url)
        graph.add((resource_uri, FOAF.depiction, Literal(profile_picture_url)))

    # print graph.serialize(format='turtle')
    # print graph.serialize(format='xml')

    insert_by_post(graph)


def update_person_object_triples(old_slug, new_slug):
    old_resource_uri = resource_uri_for_person_from_slug(old_slug)
    new_resource_uri = resource_uri_for_person_from_slug(new_slug)

    update_resource_uri(old_resource_uri, new_resource_uri)


def delete_person_rdf(person):
    resource_uri = resource_uri_for_person_from_slug(person.slug)
    delete_resource(resource_uri)


def save_job_as_rdf(job):
    graph = Graph()

    graph.bind("foaf", FOAF)
    graph.bind("dc", DC)
    graph.bind("xsd", XSD)
    graph.bind("swrcfe", SWRCFE)

    resource_uri = URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'jobs', job.id))

    graph.add((resource_uri, RDF.type, SWRCFE.Job))

    graph.add((
        resource_uri,
        SWRCFE.doneBy,
        resource_uri_for_person_from_slug(job.person.slug)))

    print graph.serialize(format='n3')

    insert_by_post(graph)


def delete_job_rdf(job):
    print 'delete'
