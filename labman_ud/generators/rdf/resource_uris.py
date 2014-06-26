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
