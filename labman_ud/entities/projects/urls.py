# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'entities.projects.views.project_index', name='project_index'),
    url(r'^info/(\S+)$', 'entities.projects.views.project_info', name='project_info'),

    url(r'^tag/(?P<tag_slug>\S+)/$', 'entities.projects.views.project_index', name='view_project_tag'),
    url(r'^status/(?P<status_slug>\S+)/$', 'entities.projects.views.project_index', name='view_project_status'),
    url(r'^project_type/(?P<project_type_slug>\S+)/$', 'entities.projects.views.project_index', name='view_project_type'),

    url(r'^query/(?P<query_string>\D+)/$', 'entities.projects.views.project_index', name='view_project_query'),

    url(r'^tag_cloud/$', 'entities.projects.views.project_tag_cloud', name='project_tag_cloud'),
)

urlpatterns += staticfiles_urlpatterns()
