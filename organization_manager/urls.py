from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'organization_manager.views.index', name = 'organization_index'),
    url(r'^nueva/$', 'organization_manager.views.add_organization', name = 'add_organization'),
    url(r'^editar/(\S+)$', 'organization_manager.views.edit_organization', name = 'edit_organization'),
    url(r'^eliminar/(\S+)$', 'organization_manager.views.delete_organization', name = 'delete_organization'),
)

urlpatterns += staticfiles_urlpatterns()
