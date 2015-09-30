# -*- encoding: utf-8 -*-

from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *


###		Organization
####################################################################################################

def save_organization_as_rdf(organization):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_organization_from_slug(organization.slug)

    # Define type and label of resource
    organization_type = organization.organization_type

    if organization_type == 'Association':
        graph.add((resource_uri, RDF.type, SWRCFE.Association))
    elif organization_type == 'Educational organization':
        graph.add((resource_uri, RDF.type, SWRCFE.EducationalOrganization))
    elif organization_type == 'Enterprise':
        graph.add((resource_uri, RDF.type, SWRCFE.Enterprise))
    elif organization_type == 'Foundation':
        graph.add((resource_uri, RDF.type, SWRCFE.Foundation))
    elif organization_type == 'Public administration':
        graph.add((resource_uri, RDF.type, SWRCFE.PublicAdministration))
    elif organization_type == 'Research group':
        graph.add((resource_uri, RDF.type, SWRCFE.ResearchGroup))
    elif organization_type == 'University':
        graph.add((resource_uri, RDF.type, SWRCFE.University))
    else:
        graph.add((resource_uri, RDF.type, SWRCFE.Organization))

    graph.add((resource_uri, RDFS.label, Literal(organization.full_name)))

    # Sub Organization Of is optional
    if organization.sub_organization_of:
        graph.add((resource_uri, DCTERMS.isPartOf, Literal(organization.sub_organization_of)))

    # Full name is required
    graph.add((resource_uri, DC.title, Literal(organization.full_name)))

    # Short name is always generated
    graph.add((resource_uri, DC.identifier, Literal(organization.short_name)))

    # Country is optional
    if organization.country:
        graph.add((resource_uri, FOAF.based_near, resource_uri_for_country_from_slug(organization.country.slug)))

    # Homepage is optional
    if organization.homepage:
        graph.add((resource_uri, FOAF.homepage, URIRef(organization.homepage)))

    # Logo is optional
    if organization.logo:
        logo_url = '%s%s' % (getattr(settings, 'BASE_URL', None), organization.logo.url)
        graph.add((resource_uri, FOAF.depiction, Literal(logo_url)))

    # If organization is a Unit (Research Group for which labman is deployed), generate triples with its heads
    if organization.unit.all():
        try:
            save_unit_as_rdf(organization.unit.all()[0])
        except:
            pass

    # Generate triples for organization's see also links
    for see_also_link in organization.see_also_links.all():
        save_organization_see_also_as_rdf(see_also_link)

    insert_by_post(graph)


def delete_organization_rdf(organization):
    resource_uri = resource_uri_for_organization_from_slug(organization.slug)

    delete_resource(resource_uri)


###		OrganizationSeeAlso
####################################################################################################

def save_organization_see_also_as_rdf(organization_see_also):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_organization_from_slug(organization_see_also.organization.slug)

    graph.add((resource_uri, RDFS.seeAlso, URIRef(organization_see_also.see_also)))

    insert_by_post(graph)


def delete_organization_see_also_rdf(organization_see_also):
    resource_uri = resource_uri_for_organization_from_slug(organization_see_also.organization.slug)

    delete_resources_with_predicate(resource_uri, RDFS.seeAlso)


###		Unit
####################################################################################################

def save_unit_as_rdf(unit):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_organization_from_slug(unit.organization.slug)

    graph.add((resource_uri, RDFS.seeAlso, resource_uri_for_person_from_slug(unit.head.slug)))

    insert_by_post(graph)


def delete_unit_rdf(unit):
    resource_uri = resource_uri_for_organization_from_slug(unit.organization.slug)

    delete_resources_with_predicate(resource_uri, SWRCFE.headOfUnit)
