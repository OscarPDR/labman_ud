# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'persons.views.person_index', name='person_index'),
    url(r'^info/(\S+)$', 'persons.views.person_info', name='person_info'),
)

urlpatterns += staticfiles_urlpatterns()
