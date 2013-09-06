# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'entities.persons.views.person_index', name='person_index'),
    url(r'^info/(\S+)$', 'entities.persons.views.person_info', name='person_info'),
    url(r'^members/(?P<member_slug>\S+)/$', 'entities.persons.views.member_info', name='member_info'),
    url(r'^members/$', 'entities.persons.views.members', name='members'),
)

urlpatterns += staticfiles_urlpatterns()
