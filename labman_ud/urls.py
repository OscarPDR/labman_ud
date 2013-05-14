
##########################################
###         PRODUCTION URLS FOR labman_ud
###
### Last update: 14-05-2013
##########################################

from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.sites.models import Site


admin.autodiscover()

admin.site.unregister(Site)


urlpatterns = patterns('',
    url(r'^$', 'labman_ud.views.home', name='home'),
    url(r'^login/$', 'django.contrib.auth.views.login'),
    url(r'^logout/$', 'labman_ud.views.logout_view', name='logout_view'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    url(r'^organizations/', include('entities.organizations.urls')),
    url(r'^persons/', include('entities.persons.urls')),
    url(r'^projects/', include('entities.projects.urls')),
    url(r'^funding_programs/', include('entities.funding_programs.urls')),

    url(r'^charts/', include('charts.urls')),
    url(r'^semantic_search/', include('semantic_search.urls')),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'labman_ud.views.view404'
