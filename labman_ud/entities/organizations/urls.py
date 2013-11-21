# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'entities.organizations.views.organization_index', name='organization_index'),
    url(r'^info/(\S+)$', 'entities.organizations.views.organization_info', name='organization_info'),

    url(r'^query/(?P<query_string>\D+)/$', 'entities.organizations.views.organization_index', name='view_organization_query'),

    url(r'^organization_type/(?P<organization_type_slug>\S+)/$', 'entities.organizations.views.organization_index', name='view_organization_type'),
)

urlpatterns += staticfiles_urlpatterns()
