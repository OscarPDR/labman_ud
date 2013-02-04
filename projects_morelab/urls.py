from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'projects_morelab.views.home', name = 'home'),
    url(r'^$', 'projects_morelab.views.login', name = 'login'),
    url(r'^logout/$', 'projects_morelab.views.logout', name = 'logout'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^organizations/', include('organization_manager.urls')),
    url(r'^employees/', include('employee_manager.urls')),
    url(r'^projects/', include('project_manager.urls')),

    # Just for development purposes, serve in another way in production
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()
