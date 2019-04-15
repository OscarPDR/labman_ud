# -*- encoding: utf-8 -*-

from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.base import RedirectView

from labman_ud.util import FeedWrapper
from entities.publications.views import LatestPublicationsFeed

import entities.publications.views as views

urlpatterns = [
    url(r'^$', views.publication_index, name='publication_index'),
    url(r'^$', RedirectView.as_view(url='1/', permanent=False)),
    url(r'^filtered/(?P<page>\d+)/$', views.publication_index, name='filtered_publication_query'),
    url(r'^(?P<page>\d+)/$', views.publication_index, name='publication_index'),

    url(r'^info/(?P<publication_slug>\S+)/related_projects/$', views.publication_related_projects, name='publication_related_projects'),
    url(r'^info/(?P<publication_slug>\S+)/related_publications/$', views.publication_related_publications, name='publication_related_publications'),
    url(r'^info/(?P<publication_slug>\S+)/extended_information/$', views.publication_ext_info, name='publication_ext_info'),
    url(r'^info/(?P<publication_slug>\S+)/$', views.publication_info, name='publication_info'),

    url(r'^feed/$', FeedWrapper(LatestPublicationsFeed()), name='publication_feed'),

    url(r'^tag/(?P<tag_slug>\S+)/$', views.publication_index, name='view_publication_tag'),
    url(r'^publication_type/(?P<publication_type>\S+)/$', views.publication_index, name='view_publication_type'),

    url(r'^phd_dissertations/$', views.phd_dissertations_index, name='phd_dissertations_index'),

    url(r'^query/(?P<query_string>.+)/$', views.publication_index, name='view_publication_query'),
]

urlpatterns += staticfiles_urlpatterns()
