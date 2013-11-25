# coding: utf-8

from django.conf import settings


def global_vars(request):
    return {getattr(settings, 'RDF_URI', None)}
