# -*- encoding: utf-8 -*-


from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *

# print graph.serialize(format='turtle')
# print graph.serialize(format='n3')
# print graph.serialize(format='xml')


###########################################################################
# Model: Book
###########################################################################

def save_book_as_rdf(book):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(book.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.Book))
    graph.add((resource_uri, RDFS.label, Literal(book.title)))

    # Title is required
    graph.add((resource_uri, DC.title, Literal(book.title)))

    # Abstract is optional
    if book.abstract:
        graph.add((resource_uri, BIBO.abstract, Literal(book.abstract)))

    # DOI is optional
    if book.doi:
        graph.add((resource_uri, BIBO.doi, Literal(book.doi)))

    # Published is optional
    if book.published:
        graph.add((resource_uri, DC.date, Literal(book.published, datatype=XSD.date)))

    # Year is required
    graph.add((resource_uri, SWRCFE.publicationYear, Literal(book.year)))

    # PDF is optional
    if book.pdf:
        pdf_url = '%s%s' % (getattr(settings, 'BASE_URL', None), book.pdf.url)
        graph.add((resource_uri, RDFS.seeAlso, URIRef(pdf_url)))

    # Language is required
    graph.add((resource_uri, DC.language, resource_uri_for_language_from_slug(book.language.slug)))

    # Bibtex is optional
    if book.bibtex:
        graph.add((resource_uri, SWRCFE.bibtex, Literal(book.bibtex)))

    # Publisher is optional
    if book.publisher:
        graph.add((resource_uri, DCTERMS.publisher, Literal(book.publisher)))

    # Place is optional
    if book.place:
        graph.add((resource_uri, DCTERMS.spatial, Literal(book.place)))

    # Volume is optional
    if book.volume:
        graph.add((resource_uri, BIBO.volume, Literal(book.volume)))

    # ISBN is optional
    if book.isbn:
        graph.add((resource_uri, BIBO.isbn, Literal(book.isbn)))

    # Edition is optional
    if book.edition:
        graph.add((resource_uri, BIBO.edition, Literal(book.edition)))

    # Series is optional
    if book.series:
        graph.add((resource_uri, SWRCFE.series, Literal(book.series)))

    # Series number is optional
    if book.series_number:
        graph.add((resource_uri, SWRCFE.seriesNumber, Literal(book.series_number)))

    # Number of pages is optional
    if book.number_of_pages:
        graph.add((resource_uri, BIBO.numPages, Literal(book.number_of_pages)))

    # Number of volumes is optional
    if book.number_of_volumes:
        graph.add((resource_uri, BIBO.numVolumes, Literal(book.number_of_volumes)))

    insert_by_post(graph)


# def update_person_object_triples(old_slug, new_slug):
#     old_resource_uri = resource_uri_for_person_from_slug(old_slug)
#     new_resource_uri = resource_uri_for_person_from_slug(new_slug)

#     update_resource_uri(old_resource_uri, new_resource_uri)


def delete_book_rdf(book):
    resource_uri = resource_uri_for_publication_from_slug(book.slug)

    delete_resource(resource_uri)


###########################################################################
# Model: PublicationSeeAlso
###########################################################################

# def save_person_see_also_as_rdf(person_see_also):
#     graph = create_namespaced_graph()

#     resource_uri = resource_uri_for_person_from_slug(person_see_also.person.slug)

#     graph.add((resource_uri, RDFS.seeAlso, URIRef(person_see_also.see_also)))

#     insert_by_post(graph)


# def delete_person_see_also_rdf(person_see_also):
#     resource_uri = resource_uri_for_person_from_slug(person_see_also.person.slug)

#     delete_resources_with_predicate(resource_uri, RDFS.seeAlso)
