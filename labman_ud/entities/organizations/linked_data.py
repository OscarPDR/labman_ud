# -*- encoding: utf-8 -*-


from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *


###########################################################################
# Model: Organization
###########################################################################

def save_organization_as_rdf(organization):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_organization_from_slug(organization.slug)

    # Define type and label of resource
    organization_type = organization.organization_type

    if organization_type == 'Company':
        graph.add((resource_uri, RDF.type, SWRCFE.Enterprise))
    elif organization_type == 'Educational organization':
        graph.add((resource_uri, RDF.type, SWRCFE.TODO))
    elif organization_type == 'Foundation':
        graph.add((resource_uri, RDF.type, SWRCFE.TODO))
    elif organization_type == 'Public administration':
        graph.add((resource_uri, RDF.type, SWRCFE.TODO))
    elif organization_type == 'Research centre':
        graph.add((resource_uri, RDF.type, SWRCFE.ResearchGroup))
    elif organization_type == 'University':
        graph.add((resource_uri, RDF.type, SWRCFE.University))
    else:
        graph.add((resource_uri, RDF.type, SWRCFE.Organization))

    graph.add((resource_uri, RDFS.label, Literal(organization.full_name)))

    # Sub Organization Of is optional
    if organization.sub_organization_of:
        graph.add((resource_uri, DCTERMS.isPartOf, Literal(organization.sub_organization_of)))

    # Full name is always generated
    graph.add((resource_uri, FOAF.name, Literal(person.full_name)))

    # Logo is optional
    if organization.logo:
        logo_url = '%s%s' % (getattr(settings, 'BASE_URL', None), organization.logo.url)
        graph.add((resource_uri, FOAF.depiction, Literal(logo_url)))

    insert_by_post(graph)


def delete_organization_rdf(organization):
    resource_uri = resource_uri_for_organization_from_slug(organization.slug)

    delete_resource(resource_uri)
