# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from labman_ud.util import FeedWrapper
from entities.publications.views import LatestPublicationsFeed

urlpatterns = patterns('',
    url(r'^$', 'entities.publications.views.publication_index', name='publication_index'),
    url(r'^info/(\S+)/related/projects/$', 'entities.publications.views.publication_related_projects', name='publication_related_projects'),
    url(r'^info/(\S+)/related/publications/$', 'entities.publications.views.publication_related_publications', name='publication_related_publications'),
    url(r'^info/(\S+)$', 'entities.publications.views.publication_info', name='publication_info'),

    url(r'^feed/$', FeedWrapper(LatestPublicationsFeed()), name='publication_feed'),

    url(r'^tag/(?P<tag_slug>\S+)/$', 'entities.publications.views.publication_index', name='view_publication_tag'),
    url(r'^publication_type/(?P<publication_type>\S+)/$', 'entities.publications.views.publication_index', name='view_publication_type'),

    url(r'^phd_dissertations/$', 'entities.publications.views.phd_dissertations_index', name='phd_dissertations_index'),

    url(r'^query/(?P<query_string>.+)/$', 'entities.publications.views.publication_index', name='view_publication_query'),

    url(r'^tag_cloud/$', 'entities.publications.views.publication_tag_cloud', name='publication_tag_cloud'),
)

urlpatterns += staticfiles_urlpatterns()
