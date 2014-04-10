# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from entities.news.views import LatestNewsFeed

urlpatterns = patterns('',
    url(r'^$', 'entities.news.views.news_index', name='news_index'),
    url(r'^view/(?P<news_slug>\S+)/$', 'entities.news.views.view_news', name='view_news'),
    url(r'^feed/$', LatestNewsFeed(), name='news_feed')
)

urlpatterns += staticfiles_urlpatterns()
