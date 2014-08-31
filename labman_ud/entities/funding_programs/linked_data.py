# -*- encoding: utf-8 -*-


from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *


###########################################################################
# Model: FundingProgram
###########################################################################

def save_funding_program_as_rdf(funding_program):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_funding_program_from_slug(funding_program.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRCFE.FundingProgram))
    graph.add((resource_uri, RDFS.label, Literal(funding_program.full_name)))

    # Full name is required
    graph.add((resource_uri, DC.title, Literal(funding_program.full_name)))

    # Short name is always generated
    graph.add((resource_uri, FOAF.name, Literal(funding_program.full_name)))

    insert_by_post(graph)


def update_person_object_triples(old_slug, new_slug):
    old_resource_uri = resource_uri_for_person_from_slug(old_slug)
    new_resource_uri = resource_uri_for_person_from_slug(new_slug)

    update_resource_uri(old_resource_uri, new_resource_uri)


def delete_person_rdf(person):
    resource_uri = resource_uri_for_person_from_slug(person.slug)

    delete_resource(resource_uri)


###########################################################################
# Model: PersonSeeAlso
###########################################################################

def save_person_see_also_as_rdf(person_see_also):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_person_from_slug(person_see_also.person.slug)

    graph.add((resource_uri, RDFS.seeAlso, URIRef(person_see_also.see_also)))

    insert_by_post(graph)


def delete_person_see_also_rdf(person_see_also):
    resource_uri = resource_uri_for_person_from_slug(person_see_also.person.slug)

    delete_resources_with_predicate(resource_uri, RDFS.seeAlso)


###########################################################################
# Model: AccountProfile
###########################################################################


def save_account_profile_as_rdf(account_profile):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_account_profile_from_id(account_profile.id)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRCFE.AccountProfile))

    label = '%s\'s profile at %s' % (account_profile.person.full_name, account_profile.network.name)
    graph.add((resource_uri, RDFS.label, Literal(label)))

    # Profile ID is required
    graph.add((resource_uri, SWRCFE.profileId, Literal(account_profile.profile_id)))

    graph.add((resource_uri_for_person_from_slug(account_profile.person.slug), SWRCFE.holds, resource_uri))

    insert_by_post(graph)


def delete_account_profile_rdf(account_profile):
    resource_uri = resource_uri_for_account_profile_from_id(account_profile.id)

    delete_resource(resource_uri)


###########################################################################
# Model: Nickname
###########################################################################

def save_nickname_as_rdf(nickname):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_person_from_slug(nickname.person.slug)

    graph.add((resource_uri, FOAF.nick, Literal(nickname.nickname)))

    insert_by_post(graph)


def delete_nickname_rdf(nickname):
    resource_uri = resource_uri_for_person_from_slug(nickname.person.slug)

    delete_resources_with_predicate(resource_uri, FOAF.nick)


###########################################################################
# Model: Job
###########################################################################


def save_job_as_rdf(job):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_job_from_id(job.id)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRCFE.Job))

    label = '%s\'s job as %s at %s' % (job.person.full_name, job.position, job.organization.short_name)
    graph.add((resource_uri, RDFS.label, Literal(label)))

    graph.add((resource_uri_for_person_from_slug(job.person.slug), SWRCFE.hasJob, resource_uri))

    # Person is required
    graph.add((resource_uri, SWRCFE.doneBy, resource_uri_for_person_from_slug(job.person.slug)))

    # Organization is required
    graph.add((resource_uri, SWRCFE.carriedOutIn, resource_uri_for_organization_from_slug(job.organization.slug)))

    # Position is optional
    if job.position:
        graph.add((resource_uri, SWRCFE.position, Literal(job.position)))

    # Description is optional
    if job.description:
        graph.add((resource_uri, DC.description, Literal(job.description)))

    # Start date is optional
    if job.start_date:
        graph.add((resource_uri, SWRCFE.jobStartDate, Literal(job.start_date, datatype=XSD.date)))

    # End date is optional
    if job.end_date:
        graph.add((resource_uri, SWRCFE.jobEndDate, Literal(job.end_date, datatype=XSD.date)))

    graph.add((
        resource_uri,
        SWRCFE.doneBy,
        resource_uri_for_person_from_slug(job.person.slug)))

    insert_by_post(graph)


def delete_job_rdf(job):
    resource_uri = resource_uri_for_job_from_id(job.id)

    delete_resource(resource_uri)
