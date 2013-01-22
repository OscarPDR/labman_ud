from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'organization_manager.views.organization_index', name = 'organization_index'),
    url(r'^add/$', 'organization_manager.views.add_organization', name = 'add_organization'),
    url(r'^info/(\S+)$', 'organization_manager.views.info_organization', name = 'info_organization'),
    url(r'^edit/(\S+)$', 'organization_manager.views.edit_organization', name = 'edit_organization'),
    url(r'^delete/(\S+)$', 'organization_manager.views.delete_organization', name = 'delete_organization'),
)

urlpatterns += staticfiles_urlpatterns()
