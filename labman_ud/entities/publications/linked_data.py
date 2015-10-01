# -*- encoding: utf-8 -*-


from rdflib import Literal

from django.conf import settings

from generators.rdf.rdf_management import *
from generators.rdf.resource_uris import *

from entities.utils.models import Language


###		Publication
####################################################################################################

def save_publication_as_rdf(publication):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(publication.slug)

    # Title is required
    graph.add((resource_uri, DC.title, Literal(publication.title)))

    # Abstract is optional
    if publication.abstract:
        graph.add((resource_uri, BIBO.abstract, Literal(publication.abstract)))

    # DOI is optional
    if publication.doi:
        graph.add((resource_uri, BIBO.doi, Literal(publication.doi)))

    # Published is optional
    if publication.published:
        graph.add((resource_uri, DC.date, Literal(publication.published, datatype=XSD.date)))

    # Year is required
    graph.add((resource_uri, SWRCFE.publicationYear, Literal(publication.year)))

    # PDF is optional
    if publication.pdf:
        pdf_url = '%s%s' % (getattr(settings, 'BASE_URL', None), publication.pdf.url)
        graph.add((resource_uri, RDFS.seeAlso, URIRef(pdf_url)))

    # Language is required
    if publication.language:
        graph.add((resource_uri, DC.language, resource_uri_for_language_from_slug(publication.language.slug)))

    else:
        english = Language.objects.get_or_create(name='English')[0]
        graph.add((resource_uri, DC.language, resource_uri_for_language_from_slug(english.slug)))

    # Bibtex is optional
    if publication.bibtex:
        graph.add((resource_uri, SWRCFE.bibtex, Literal(publication.bibtex)))

    if len(publication.authors.all()) > 0:
        for publication_author in publication.publicationauthor_set.all():
            graph.add((resource_uri, DC.creator, resource_uri_for_person_from_slug(publication_author.author.slug)))

            # Save publication author object

    if len(publication.editors.all()) > 0:
        for publication_editor in publication.publicationeditor_set.all():
            graph.add((resource_uri, DC.creator, resource_uri_for_person_from_slug(publication_editor.editor.slug)))

            # Save publication editor object

    if len(publication.tags.all()) > 0:
        for publication_tag in publication.publicationtag_set.all():
            graph.add((resource_uri, DC.subject, resource_uri_for_tag_from_slug(publication_tag.tag.slug)))

    insert_by_post(graph)


def update_publication_object_triples(old_slug, new_slug):
    old_resource_uri = resource_uri_for_publication_from_slug(old_slug)
    new_resource_uri = resource_uri_for_publication_from_slug(new_slug)

    update_resource_uri(old_resource_uri, new_resource_uri)


###		BookSection
####################################################################################################

def save_book_section_as_rdf(book_section):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(book_section.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.InBook))
    graph.add((resource_uri, RDFS.label, Literal(book_section.title)))

    # Pages is optional
    if book_section.pages:
        graph.add((resource_uri, BIBO.pages, Literal(book_section.pages)))

    # Short title is optional
    if book_section.short_title:
        graph.add((resource_uri, SWRCFE.publicationShortTitle, Literal(book_section.short_title)))

    # Parent book is always present
    graph.add((resource_uri, DCTERMS.isPartOf, resource_uri_for_publication_from_slug(book_section.parent_book.slug)))

    # Presented at is optional
    # TODO: reference to event page

    insert_by_post(graph)


def delete_book_section_rdf(book_section):
    resource_uri = resource_uri_for_publication_from_slug(book_section.slug)

    delete_resource(resource_uri)


###		Book
####################################################################################################

def save_book_as_rdf(book):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(book.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.Book))
    graph.add((resource_uri, RDFS.label, Literal(book.title)))

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


def delete_book_rdf(book):
    resource_uri = resource_uri_for_publication_from_slug(book.slug)

    delete_resource(resource_uri)


###		ConferencePaper
####################################################################################################

def save_conference_paper_as_rdf(conference_paper):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(conference_paper.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.InProceedings))
    graph.add((resource_uri, RDFS.label, Literal(conference_paper.title)))

    # Pages is optional
    if conference_paper.pages:
        graph.add((resource_uri, BIBO.pages, Literal(conference_paper.pages)))

    # Short title is optional
    if conference_paper.short_title:
        graph.add((resource_uri, SWRCFE.publicationShortTitle, Literal(conference_paper.short_title)))

    # Parent proceedings is always present
    graph.add((resource_uri, DCTERMS.isPartOf, resource_uri_for_publication_from_slug(conference_paper.parent_proceedings.slug)))

    # Presented at is optional
    # TODO: reference to event page

    insert_by_post(graph)


def delete_conference_paper_rdf(conference_paper):
    resource_uri = resource_uri_for_publication_from_slug(conference_paper.slug)

    delete_resource(resource_uri)


###		Proceedings
####################################################################################################

def save_proceedings_as_rdf(proceedings):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(proceedings.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.Proceedings))
    graph.add((resource_uri, RDFS.label, Literal(proceedings.title)))

    # Publisher is optional
    if proceedings.publisher:
        graph.add((resource_uri, DCTERMS.publisher, Literal(proceedings.publisher)))

    # Place is optional
    if proceedings.place:
        graph.add((resource_uri, DCTERMS.spatial, Literal(proceedings.place)))

    # Volume is optional
    if proceedings.volume:
        graph.add((resource_uri, BIBO.volume, Literal(proceedings.volume)))

    # ISBN is optional
    if proceedings.isbn:
        graph.add((resource_uri, BIBO.isbn, Literal(proceedings.isbn)))

    # Series is optional
    if proceedings.series:
        graph.add((resource_uri, SWRCFE.series, Literal(proceedings.series)))

    insert_by_post(graph)


def delete_proceedings_rdf(proceedings):
    resource_uri = resource_uri_for_publication_from_slug(proceedings.slug)

    delete_resource(resource_uri)


###		JournalArticle
####################################################################################################

def save_journal_article_as_rdf(journal_article):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(journal_article.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.Article))
    graph.add((resource_uri, RDFS.label, Literal(journal_article.title)))

    # Pages is optional
    if journal_article.pages:
        graph.add((resource_uri, BIBO.pages, Literal(journal_article.pages)))

    # Short title is optional
    if journal_article.short_title:
        graph.add((resource_uri, SWRCFE.publicationShortTitle, Literal(journal_article.short_title)))

    # Parent journal is always present
    graph.add((resource_uri, DCTERMS.isPartOf, resource_uri_for_publication_from_slug(journal_article.parent_journal.slug)))

    # Individually published is optional
    # TODO:

    insert_by_post(graph)


def delete_journal_article_rdf(journal_article):
    resource_uri = resource_uri_for_publication_from_slug(journal_article.slug)

    delete_resource(resource_uri)


###		Journal
####################################################################################################

def save_journal_as_rdf(journal):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(journal.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.Journal))
    graph.add((resource_uri, RDFS.label, Literal(journal.title)))

    # Publisher is optional
    if journal.publisher:
        graph.add((resource_uri, DCTERMS.publisher, Literal(journal.publisher)))

    # Place is optional
    if journal.place:
        graph.add((resource_uri, DCTERMS.spatial, Literal(journal.place)))

    # Volume is optional
    if journal.volume:
        graph.add((resource_uri, BIBO.volume, Literal(journal.volume)))

    # ISSN is optional
    if journal.issn:
        graph.add((resource_uri, BIBO.issn, Literal(journal.issn)))

    # Issue is optional
    if journal.issue:
        graph.add((resource_uri, BIBO.issue, Literal(journal.issue)))

    # Journal abbreviation is optional
    if journal.journal_abbreviation:
        graph.add((resource_uri, SWRCFE.journalAbbreviation, Literal(journal.journal_abbreviation)))

    # Quartile is optional
    if journal.quartile:
        graph.add((resource_uri, SWRCFE.quartile, Literal(journal.quartile)))

    # Impact factor is optional
    if journal.impact_factor:
        graph.add((resource_uri, SWRCFE.impactFactor, Literal(journal.impact_factor)))

    insert_by_post(graph)


def delete_journal_rdf(journal):
    resource_uri = resource_uri_for_publication_from_slug(journal.slug)

    delete_resource(resource_uri)


###		MagazineArticle
####################################################################################################

def save_magazine_article_as_rdf(magazine_article):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(magazine_article.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.UnrefereedArticle))
    graph.add((resource_uri, RDFS.label, Literal(magazine_article.title)))

    # Pages is optional
    if magazine_article.pages:
        graph.add((resource_uri, BIBO.pages, Literal(magazine_article.pages)))

    # Short title is optional
    if magazine_article.short_title:
        graph.add((resource_uri, SWRCFE.publicationShortTitle, Literal(magazine_article.short_title)))

    # Parent magazine is always present
    graph.add((resource_uri, DCTERMS.isPartOf, resource_uri_for_publication_from_slug(magazine_article.parent_magazine.slug)))

    # Individually published is optional
    # TODO:

    insert_by_post(graph)


def delete_magazine_article_rdf(magazine_article):
    resource_uri = resource_uri_for_publication_from_slug(magazine_article.slug)

    delete_resource(resource_uri)


###		Magazine
####################################################################################################

def save_magazine_as_rdf(magazine):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(magazine.slug)

    # Define type and label of resource
    graph.add((resource_uri, RDF.type, SWRC.Magazine))
    graph.add((resource_uri, RDFS.label, Literal(magazine.title)))

    # Publisher is optional
    if magazine.publisher:
        graph.add((resource_uri, DCTERMS.publisher, Literal(magazine.publisher)))

    # Place is optional
    if magazine.place:
        graph.add((resource_uri, DCTERMS.spatial, Literal(magazine.place)))

    # Volume is optional
    if magazine.volume:
        graph.add((resource_uri, BIBO.volume, Literal(magazine.volume)))

    # ISSN is optional
    if magazine.issn:
        graph.add((resource_uri, BIBO.issn, Literal(magazine.issn)))

    # Issue is optional
    if magazine.issue:
        graph.add((resource_uri, BIBO.issue, Literal(magazine.issue)))

    insert_by_post(graph)


def delete_magazine_rdf(magazine):
    resource_uri = resource_uri_for_publication_from_slug(magazine.slug)

    delete_resource(resource_uri)


###		PublicationSeeAlso
####################################################################################################

def save_publication_see_also_as_rdf(publication_see_also):
    graph = create_namespaced_graph()

    resource_uri = resource_uri_for_publication_from_slug(publication_see_also.publication.slug)

    graph.add((resource_uri, RDFS.seeAlso, URIRef(publication_see_also.see_also)))

    insert_by_post(graph)


def delete_publication_see_also_rdf(publication_see_also):
    resource_uri = resource_uri_for_publication_from_slug(publication_see_also.publication.slug)

    delete_resources_with_predicate(resource_uri, RDFS.seeAlso)
