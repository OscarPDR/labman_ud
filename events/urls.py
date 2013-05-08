# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'events.views.project_index', name='event_index'),
    url(r'^add/$', 'events.views.add_event', name='add_event'),
    url(r'^info/(\S+)$', 'events.views.event_info', name='event_info'),
    url(r'^edit/(\S+)$', 'events.views.edit_event', name='edit_event'),
    url(r'^delete/(\S+)$', 'events.views.delete_event', name='delete_event'),
)

urlpatterns += staticfiles_urlpatterns()
