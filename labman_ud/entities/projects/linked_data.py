# -*- encoding: utf-8 -*-


from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *


###########################################################################
# Model: Project
###########################################################################

def save_project_as_rdf(project):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_project_from_slug(project.slug)

    # Define type and label of resource

    if project.project_type == 'Applied research project':
        graph.add((resource_uri, RDF.type, SWRCFE.AppliedResearchProject))
    elif project.project_type == 'Development project':
        graph.add((resource_uri, RDF.type, SWRC.DevelopmentProject))
    elif project.project_type == 'External project':
        graph.add((resource_uri, RDF.type, SWRCFE.ExternalProject))
    elif project.project_type == 'Innovation project':
        graph.add((resource_uri, RDF.type, SWRCFE.InnovationProject))
    elif project.project_type == 'Internal project':
        graph.add((resource_uri, RDF.type, SWRCFE.InternalProject))
    elif project.project_type == 'Research roject':
        graph.add((resource_uri, RDF.type, SWRC.ResearchProject))
    else:
        graph.add((resource_uri, RDF.type, SWRC.Project))

    graph.add((resource_uri, RDFS.label, Literal(project.full_name)))

    # Full name is required
    graph.add((resource_uri, DC.title, Literal(project.full_name)))

    # Short name is always present
    graph.add((resource_uri, DC.identifier, Literal(project.short_name)))

    # Description is optional
    if project.description:
        graph.add((resource_uri, DC.description, Literal(project.description)))

    # Homepage is optional
    if project.homepage:
        graph.add((resource_uri, FOAF.homepage, Literal(project.homepage)))

    # Start month and year are required
    start_date_string = u'%s-%s' % (project.start_year, project.start_month)
    graph.add((resource_uri, SWRCFE.startDate, Literal(start_date_string, datatype=XSD.gYearMonth)))

    # End month and year are required
    end_date_string = u'%s-%s' % (project.end_year, project.end_month)
    graph.add((resource_uri, SWRCFE.endDate, Literal(end_date_string, datatype=XSD.gYearMonth)))

    # Status is required
    graph.add((resource_uri, SWRCFE.status, Literal(project.status)))

    # Logo is optional
    if project.logo:
        project_logo_url = '%s%s' % (getattr(settings, 'BASE_URL', None), project.logo.url)
        graph.add((resource_uri, FOAF.depiction, Literal(project_logo_url)))

    # TODO: Private funding details

    # Generate triples for assigned people
    if len(project.assignedperson_set.all()) > 0:
        for assigned_person in project.assignedperson_set.all():
            save_assigned_person_as_rdf(assigned_person)

    # Project leader is required
    graph.add((resource_uri, SWRCFE.projectLeader, resource_uri_for_organization_from_slug(project.project_leader.slug)))

    # Generate triples for consortium members
    if len(project.consortiummember_set.all()) > 0:
        for consortium_member in project.consortiummember_set.all():
            graph.add((resource_uri, SWRCFE.carriedOutBy, resource_uri_for_organization_from_slug(consortium_member.organization.slug)))

    # Generate triples for related publications
    if len(project.relatedpublication_set.all()) > 0:
        for related_publication in project.relatedpublication_set.all():
            graph.add((resource_uri, SWRCFE.relatedPublication, resource_uri_for_publication_from_slug(related_publication.publication.slug)))

    # Generate triples for tags
    if len(project.tags.all()) > 0:
        for project_tag in project.tags.all():
            graph.add((resource_uri, DC.subject, resource_uri_for_tag_from_slug(project_tag.slug)))

    # Generate triples for funding
    if len(project.funding_set.all()) > 0:
        for funding in project.funding_set.all():
            save_funding_as_rdf(funding)

    insert_by_post(graph)


def update_project_object_triples(old_slug, new_slug):
    old_resource_uri = resource_uri_for_project_from_slug(old_slug)
    new_resource_uri = resource_uri_for_project_from_slug(new_slug)

    update_resource_uri(old_resource_uri, new_resource_uri)


def delete_project_rdf(project):
    resource_uri = resource_uri_for_project_from_slug(project.slug)

    delete_resource(resource_uri)


###########################################################################
# Model: ProjectSeeAlso
###########################################################################

def save_project_see_also_as_rdf(project_see_also):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_project_from_slug(project_see_also.project.slug)

    graph.add((resource_uri, RDFS.seeAlso, URIRef(project_see_also.see_also)))

    insert_by_post(graph)


def delete_project_see_also_rdf(project_see_also):
    resource_uri = resource_uri_for_project_from_slug(project_see_also.project.slug)

    delete_resources_with_predicate(resource_uri, RDFS.seeAlso)


###########################################################################
# Model: Funding
###########################################################################

def save_funding_as_rdf(funding):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_funding_from_slug(funding.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRCFE.Funding))

    funding_label = u'Funding for %s by %s' % (funding.project.short_name, funding.funding_program.full_name)
    graph.add((resource_uri, RDFS.label, Literal(funding_label)))

    # Project code is optional
    if funding.project_code:
        graph.add((resource_uri, SWRCFE.projectCode, Literal(funding.project_code)))

    # Total funds is optional
    if funding.total_funds:
        graph.add((resource_uri, SWRCFE.totalFunds, Literal(funding.total_funds, datatype=XSD.decimal)))

    # Project is required
    graph.add((resource_uri, SWRCFE.funds, resource_uri_for_project_from_slug(funding.project.slug)))

    # Funding program is required
    graph.add((resource_uri, SWRCFE.fundingProgram, resource_uri_for_funding_program_from_slug(funding.funding_program.slug)))

    # Generate triples for funding amounts
    if len(funding.fundingamount_set.all()) > 0:
        for funding_amount in funding.fundingamount_set.all():
            save_funding_amount_as_rdf(funding_amount)

    # Generate triples for funding see also links
    if len(funding.fundingseealso_set.all()) > 0:
        for funding_see_also in funding.fundingseealso_set.all():
            save_funding_see_also_as_rdf(funding_see_also)

    insert_by_post(graph)


def delete_funding_rdf(funding):
    resource_uri = resource_uri_for_funding_from_slug(funding.slug)

    delete_resource(resource_uri)


###########################################################################
# Model: FundingSeeAlso
###########################################################################

def save_funding_see_also_as_rdf(funding_see_also):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_funding_from_slug(funding_see_also.funding.slug)

    graph.add((resource_uri, RDFS.seeAlso, URIRef(funding_see_also.see_also)))

    insert_by_post(graph)


def delete_funding_see_also_rdf(funding_see_also):
    resource_uri = resource_uri_for_funding_from_slug(funding_see_also.funding.slug)

    delete_resources_with_predicate(resource_uri, RDFS.seeAlso)


###########################################################################
# Model: FundingAmount
###########################################################################

def save_funding_amount_as_rdf(funding_amount):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_funding_amount_from_id(funding_amount.id)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRCFE.FundingAmount))

    funding_amount_label = u'Funding amount for %s in %s' % (funding_amount.funding.project.short_name, funding_amount.year)
    graph.add((resource_uri, RDFS.label, Literal(funding_amount_label)))

    # Own amount is required
    graph.add((resource_uri, SWRCFE.ownAmount, Literal(funding_amount.own_amount, datatype=XSD.decimal)))

    # Year is required
    graph.add((resource_uri, SWRCFE.fundedYear, Literal(funding_amount.year, datatype=XSD.gYear)))

    # Funding is required
    graph.add((resource_uri, DCTERMS.isPartOf, resource_uri_for_funding_from_slug(funding_amount.funding.slug)))

    insert_by_post(graph)


def delete_funding_amount_rdf(funding_amount):
    resource_uri = resource_uri_for_funding_amount_from_id(funding_amount.id)

    delete_resource(resource_uri)


###########################################################################
# Model: AssignedPerson
###########################################################################

def save_assigned_person_as_rdf(assigned_person):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_assigned_person_from_id(assigned_person.id)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRCFE.AssignedPerson))

    assigned_person_label = u'%s working in %s' % (assigned_person.person.full_name, assigned_person.project.short_name)
    graph.add((resource_uri, RDFS.label, Literal(assigned_person_label)))

    # Project is required
    graph.add((resource_uri, SWRCFE.project, resource_uri_for_project_from_slug(assigned_person.project.slug)))

    # Person is required
    graph.add((resource_uri, SWRCFE.assignedPerson, resource_uri_for_person_from_slug(assigned_person.person.slug)))

    # Role is required
    graph.add((resource_uri, SWRCFE.role, Literal(assigned_person.role.name)))

    # Start date is optional
    if assigned_person.start_date:
        graph.add((resource_uri, SWRCFE.workStartDate, Literal(assigned_person.start_date, datatype=XSD.date)))

    # End date is optional
    if assigned_person.end_date:
        graph.add((resource_uri, SWRCFE.workEndDate, Literal(assigned_person.end_date, datatype=XSD.date)))

    # Description is optional
    if assigned_person.description:
        graph.add((resource_uri, DC.description, Literal(assigned_person.description)))

    insert_by_post(graph)


def delete_assigned_person_rdf(assigned_person):
    resource_uri = resource_uri_for_assigned_person_from_id(assigned_person.id)

    delete_resource(resource_uri)
