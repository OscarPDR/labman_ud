# -*- encoding: utf-8 -*-

from rdflib import Literal

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *


###		FundingProgram
####################################################################################################

# def save_funding_program_as_rdf(funding_program):
#     graph = create_namespaced_graph()

#     resource_uri = resource_uri_for_funding_program_from_slug(funding_program.slug)

#     # Define type and label of resource
#     graph.add((resource_uri, RDF.type, SWRCFE.FundingProgram))
#     graph.add((resource_uri, RDFS.label, Literal(funding_program.full_name)))

#     # Full name is required
#     graph.add((resource_uri, DC.title, Literal(funding_program.full_name)))

#     # Short name is always generated
#     graph.add((resource_uri, FOAF.name, Literal(funding_program.full_name)))

#     insert_by_post(graph)
