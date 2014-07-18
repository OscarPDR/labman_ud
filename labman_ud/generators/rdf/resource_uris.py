# -*- encoding: utf-8 -*-

from rdflib import URIRef

from django.conf import settings


def resource_uri_for_person_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'people', _slug))


def resource_uri_for_job_from_id(_id):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'jobs', _id))


def resource_uri_for_organization_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'organizations', _slug))


def resource_uri_for_account_profile_from_id(_id):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'account_profiles', _id))


def resource_uri_for_country_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'countries', _slug))


def resource_uri_for_geographical_scope_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'geographical_scopes', _slug))


def resource_uri_for_tag_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'tags', _slug))


def resource_uri_for_network_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'networks', _slug))


def resource_uri_for_publication_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'publications', _slug))


def resource_uri_for_language_from_slug(_slug):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'languages', _slug))


def resource_uri_for_publication_author_from_id(_id):
    return URIRef('%s/%s/%s' % (getattr(settings, 'RESOURCES_BASE_URL', None), 'publication_authors', _id))
