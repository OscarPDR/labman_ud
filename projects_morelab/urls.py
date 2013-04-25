
##########################################
###         PRODUCTION URLS FOR projects_morelab                      ###
###                                                                                                   ###
### Last update: 15-04-2013                                                          ###
##########################################

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'projects_morelab.views.home', name = 'home'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'projects_morelab.views.logout_view', name = 'logout_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^organizations/', include('organizations.urls')),
    url(r'^employees/', include('employees.urls')),
    url(r'^projects/', include('projects.urls')),
    url(r'^funding_programs/', include('funding_programs.urls')),

    url(r'^charts/', include('charts.urls')),
    url(r'^semantic_search/', include('semantic_search.urls')),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'projects_morelab.views.view404'
