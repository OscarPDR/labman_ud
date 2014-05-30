# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'entities.events.views.project_index', name='event_index'),
    url(r'^info/(\S+)$', 'entities.events.views.event_info', name='event_info'),
)

urlpatterns += staticfiles_urlpatterns()
