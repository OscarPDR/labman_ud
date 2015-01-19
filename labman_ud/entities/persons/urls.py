# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from labman_ud.util import FeedWrapper
from entities.persons.views import LatestUserPublicationFeed, LatestUserNewsFeed

urlpatterns = patterns('',
    url(r'^$', 'entities.persons.views.person_index', name='person_index'),
    url(r'^query/(?P<query_string>\D+)/$', 'entities.persons.views.person_index', name='view_person_query'),

    url(r'^person_info/(?P<person_slug>\S+)/$', 'entities.persons.views.determine_person_info', name='determine_person_info'),

    url(r'^info/(?P<person_slug>\S+)/$', 'entities.persons.views.person_info', name='person_info'),

    # members belonging to the organization(s)
    url(r'^members/unit/(?P<organization_slug>\S+)/$', 'entities.persons.views.members', name='members_by_organization'),
    url(r'^former_members/unit/(?P<organization_slug>\S+)/$', 'entities.persons.views.former_members', name='former_members_by_organization'),
    # list of projects by role
    url(r'^members/(?P<person_slug>\S+)/projects/(?P<role_slug>\S+)/$', 'entities.persons.views.member_projects', name='member_projects'),
    url(r'^former_members/(?P<person_slug>\S+)/projects/(?P<role_slug>\S+)/$', 'entities.persons.views.member_projects', name='former_member_projects'),
    # list of projects
    url(r'^members/(?P<person_slug>\S+)/projects/$', 'entities.persons.views.member_projects', name='member_projects'),
    url(r'^former_members/(?P<person_slug>\S+)/projects/$', 'entities.persons.views.member_projects', name='former_member_projects'),
    # BibTeX
    url(r'^members/(?P<person_slug>\S+)/publications/bibtex/$', 'entities.persons.views.member_publication_bibtex', name='member_bibtex'),
    url(r'^members/(?P<person_slug>\S+)/publications/bibtex/download$', 'entities.persons.views.member_publication_bibtex_download', name='member_bibtex_download'),
    # RSS
    url(r'^members/(?P<person_slug>\S+)/feeds/news/$', FeedWrapper(LatestUserNewsFeed()), name='member_feeds_news'),
    url(r'^members/(?P<person_slug>\S+)/feeds/publications/$', FeedWrapper(LatestUserPublicationFeed()), name='member_feeds_publications'),
    url(r'^members/(?P<person_slug>\S+)/news/$', 'entities.persons.views.member_news', name='member_news'),
    url(r'^members/(?P<person_slug>\S+)/cvn/$', 'entities.persons.views.member_spanish_cvn', name='member_spanish_cvn'),
    # Awards
    url(r'^members/(?P<person_slug>\S+)/awards/$', 'entities.persons.views.member_awards', name='member_awards'),
    url(r'^awards/(?P<award_slug>\S+)/related_projects/$', 'entities.persons.views.award_related_projects', name='award_related_projects'),
    url(r'^awards/(?P<award_slug>\S+)/related_publications/$', 'entities.persons.views.award_related_publications', name='award_related_publications'),
    url(r'^awards/(?P<award_slug>\S+)/$', 'entities.persons.views.award_info', name='award_info'),
    url(r'^awards/$', 'entities.persons.views.award_index', name='award_index'),
    # list of publications by type
    url(r'^members/(?P<person_slug>\S+)/publications/(?P<publication_type_slug>\S+)/$', 'entities.persons.views.member_publications', name='member_publications'),
    url(r'^former_members/(?P<person_slug>\S+)/publications/(?P<publication_type_slug>\S+)/$', 'entities.persons.views.member_publications', name='former_member_publications'),
    # list of publications
    url(r'^members/(?P<person_slug>\S+)/publications/$', 'entities.persons.views.member_publications', name='member_publications'),
    url(r'^former_members/(?P<person_slug>\S+)/publications/$', 'entities.persons.views.member_publications', name='former_member_publications'),
    # phd_thesis
    url(r'^members/(?P<person_slug>\S+)/phd_dissertation/$', 'entities.persons.views.member_phd_dissertation', name='member_phd_dissertation'),
    url(r'^former_members/(?P<person_slug>\S+)/phd_dissertation/$', 'entities.persons.views.member_phd_dissertation', name='former_member_phd_dissertation'),
    # list of social profiles
    url(r'^members/(?P<person_slug>\S+)/profiles/$', 'entities.persons.views.member_profiles', name='member_profiles'),
    url(r'^former_members/(?P<person_slug>\S+)/profiles/$', 'entities.persons.views.member_profiles', name='former_member_profiles'),
    # list of applicable graphs
    url(r'^members/(?P<person_slug>\S+)/graphs/$', 'entities.persons.views.member_graphs', name='member_graphs'),
    url(r'^former_members/(?P<person_slug>\S+)/graphs/$', 'entities.persons.views.member_graphs', name='former_member_graphs'),
    # member info
    url(r'^members/(?P<person_slug>\S+)/$', 'entities.persons.views.member_info', name='member_info'),
    url(r'^former_members/(?P<person_slug>\S+)/$', 'entities.persons.views.member_info', name='former_member_info'),
    # list of members
    url(r'^members/$', 'entities.persons.views.members', name='members'),
    url(r'^former_members/$', 'entities.persons.views.former_members', name='former_members'),
)

urlpatterns += staticfiles_urlpatterns()
