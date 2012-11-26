
from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
	url(r'^$', 'organization_manager.views.organization_home', name = 'organization_home'),
    url(r'^nueva/', 'organization_manager.views.organization_list', name = 'organization_list'),
    url(r'^editar/', 'organization_manager.views.organization_list', name = 'organization_list'),
)