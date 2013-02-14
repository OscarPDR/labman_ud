from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'organizations.views.organization_index', name = 'organization_index'),
    url(r'^add/$', 'organizations.views.add_organization', name = 'add_organization'),
    url(r'^info/(\S+)$', 'organizations.views.organization_info', name = 'organization_info'),
    url(r'^edit/(\S+)$', 'organizations.views.edit_organization', name = 'edit_organization'),
    url(r'^delete/(\S+)$', 'organizations.views.delete_organization', name = 'delete_organization'),
)

urlpatterns += staticfiles_urlpatterns()
