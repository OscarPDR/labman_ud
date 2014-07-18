# -*- encoding: utf-8 -*-


from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *

# print graph.serialize(format='turtle')
# print graph.serialize(format='n3')
# print graph.serialize(format='xml')


###########################################################################
# Model: Person
###########################################################################

def save_person_as_rdf(person):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_person_from_slug(person.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, FOAF.Person))
    graph.add((resource_uri, RDFS.label, Literal(person.full_name)))

    # First name is required
    graph.add((resource_uri, FOAF.firstName, Literal(person.first_name)))

    # First surname is required, second is optional
    surnames = person.first_surname

    if person.second_surname:
        surnames = '%s %s' % (surnames, person.second_surname)
    graph.add((resource_uri, FOAF.familyName, Literal(surnames)))

    # Full name is always generated
    graph.add((resource_uri, FOAF.name, Literal(person.full_name)))

    # Birth date is optional
    if person.birth_date:
        graph.add((resource_uri, FOAF.birthday, Literal(person.birth_date, datatype=XSD.date)))

    # Biography may be an empty string
    if person.safe_biography != '':
        graph.add((resource_uri, DC.description, Literal(person.safe_biography)))

    # Title is optional
    if person.title:
        graph.add((resource_uri, FOAF.title, Literal(person.title)))

    # Gender is optional
    if person.gender:
        gender = person.gender.lower()
        graph.add((resource_uri, FOAF.gender, Literal(gender)))

    # Personal website is optional
    if person.personal_website:
        graph.add((resource_uri, FOAF.homepage, URIRef(person.personal_website)))

    # Email is optional
    if person.email:
        graph.add((resource_uri, FOAF.mbox, Literal(person.email)))

    # Phone number and extension are optional (having only extension makes no sense)
    if person.phone_number:
        phone_number = person.phone_number

        if person.phone_extension:
            phone_number = '%s - ext: %s' % (phone_number, person.phone_extension)

        graph.add((resource_uri, FOAF.phone, Literal(phone_number)))

    # Belonging to the group is always present (defaults to False)
    graph.add((resource_uri, SWRCFE.isMember, Literal(person.is_active)))

    # Profile picture is optional
    if person.profile_picture:
        profile_picture_url = '%s%s' % (getattr(settings, 'BASE_URL', None), person.profile_picture.url)
        graph.add((resource_uri, FOAF.depiction, Literal(profile_picture_url)))

    # Generate triples for person's nicks
    for nick in person.nicknames.all():
        save_nickname_as_rdf(nick)

    # Generate triples for person's see also links
    for see_also_link in person.see_also_links.all():
        save_person_see_also_as_rdf(see_also_link)

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
