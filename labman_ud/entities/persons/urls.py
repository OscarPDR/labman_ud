# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'entities.persons.views.person_index', name='person_index'),
    url(r'^query/(?P<query_string>\D+)/$', 'entities.persons.views.person_index', name='view_person_query'),
    url(r'^info/(\S+)$', 'entities.persons.views.person_info', name='person_info'),

    url(r'^members/org/(?P<organization_slug>\S+)/$', 'entities.persons.views.members', name='members_by_organization'),
    url(r'^members/(?P<member_slug>\S+)/projects/$', 'entities.persons.views.member_projects', name='member_projects'),
    url(r'^members/(?P<member_slug>\S+)/publications/$', 'entities.persons.views.member_publications', name='member_publications'),
    url(r'^members/(?P<member_slug>\S+)/profiles/$', 'entities.persons.views.member_profiles', name='member_profiles'),
    url(r'^members/(?P<member_slug>\S+)/graphs/$', 'entities.persons.views.member_graphs', name='member_graphs'),
    url(r'^members/(?P<member_slug>\S+)/$', 'entities.persons.views.member_info', name='member_info'),
    url(r'^members/$', 'entities.persons.views.members', name='members'),

    url(r'^former_members/org/(?P<organization_slug>\S+)/$', 'entities.persons.views.former_members', name='former_members_by_organization'),
    url(r'^former_members/(?P<former_member_slug>\S+)/$', 'entities.persons.views.former_member_info', name='former_member_info'),
    url(r'^former_members/$', 'entities.persons.views.former_members', name='former_members'),
)

urlpatterns += staticfiles_urlpatterns()
