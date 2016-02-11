# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from labman_ud.util import FeedWrapper
from entities.projects.views import LatestProjectsFeed

import entities.projects.views as views

urlpatterns = [
    url(r'^$', views.project_index, name='project_index'),
    url(r'^filtered/$', views.project_index, name='filtered_project_query'),

    url(r'^feed/$', FeedWrapper(LatestProjectsFeed()), name='project_feed'),

    url(r'^info/(?P<project_slug>\S+)/funding_details/$', views.project_funding_details, name='project_funding_details'),
    url(r'^info/(?P<project_slug>\S+)/assigned_persons/$', views.project_assigned_persons, name='project_assigned_persons'),
    url(r'^info/(?P<project_slug>\S+)/consortium_members/$', views.project_consortium_members, name='project_consortium_members'),
    url(r'^info/(?P<project_slug>\S+)/related_publications/$', views.project_related_publications, name='project_related_publications'),
    url(r'^info/(?P<project_slug>\S+)/related_news/$', views.project_related_news, name='project_related_news'),
    url(r'^info/(?P<project_slug>\S+)/$', views.project_info, name='project_info'),

    url(r'^tag/(?P<tag_slug>\S+)/$', views.project_index, name='view_project_tag'),
    url(r'^status/(?P<status_slug>\S+)/$', views.project_index, name='view_project_status'),
    url(r'^project_type/(?P<project_type_slug>\S+)/$', views.project_index, name='view_project_type'),

    url(r'^query/(?P<query_string>.+)/$', views.project_index, name='view_project_query'),

    url(r'^tag_cloud/$', views.project_tag_cloud, name='project_tag_cloud'),
]

urlpatterns += staticfiles_urlpatterns()
