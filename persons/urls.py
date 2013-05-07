# coding: utf-8

from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'persons.views.person_index', name='person_index'),
    url(r'^add/$', 'persons.views.add_person', name='add_person'),
    url(r'^info/(\S+)$', 'persons.views.person_info', name='person_info'),
    url(r'^edit/(\S+)$', 'persons.views.edit_person', name='edit_person'),
    url(r'^delete/(?P<slug>\S+)$', 'persons.views.delete_person', name='delete_person'),
)

urlpatterns += staticfiles_urlpatterns()
