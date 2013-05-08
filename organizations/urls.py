from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'organizations.views.organization_index', name = 'organization_index'),
    url(r'^info/(\S+)$', 'organizations.views.organization_info', name = 'organization_info'),
)

urlpatterns += staticfiles_urlpatterns()
