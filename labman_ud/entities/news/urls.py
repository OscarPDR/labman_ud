# -*- encoding: utf-8 -*-

from django.conf.urls import url

from labman_ud.util import FeedWrapper
from entities.news.views import LatestNewsFeed

import entities.news.views as views


urlpatterns = [
    url(r'^$', views.news_index, name='news_index'),
    url(r'^view/(?P<news_slug>\S+)/$', views.view_news, name='view_news'),
    url(r'^feed/$', FeedWrapper(LatestNewsFeed()), name='news_feed'),
]
