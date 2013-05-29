# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'entities.publications.views.publication_index', name='publication_index'),
    url(r'^info/(\S+)$', 'entities.publications.views.publication_info', name='publication_info'),
)

urlpatterns += staticfiles_urlpatterns()
