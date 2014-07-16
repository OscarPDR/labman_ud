# -*- encoding: utf-8 -*-

from django.conf import settings


def global_vars(request):
    return {'RDF_URI': getattr(settings, 'RESOURCES_BASE_URL', None)}
