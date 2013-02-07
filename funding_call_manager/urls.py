from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'funding_call_manager.views.funding_call_index', name = 'funding_call_index'),
    url(r'^add/$', 'funding_call_manager.views.add_funding_call', name = 'add_funding_call'),
    url(r'^info/(\S+)$', 'funding_call_manager.views.info_funding_call', name = 'info_funding_call'),
    url(r'^edit/(\S+)$', 'funding_call_manager.views.edit_funding_call', name = 'edit_funding_call'),
    url(r'^delete/(\S+)$', 'funding_call_manager.views.delete_funding_call', name = 'delete_funding_call'),
)

urlpatterns += staticfiles_urlpatterns()
