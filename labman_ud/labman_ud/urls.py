# encoding: utf-8

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from .forms import LoginForm

admin.autodiscover()
#admin.site.unregister(Site)


urlpatterns = patterns('',
    url(r'^$', 'labman_ud.views.home', name='home'),

    url(r'^about/collaborations/$', 'labman_ud.views.about_collaborations', name='about_collaborations'),
    url(r'^about/prototyping/$', 'labman_ud.views.about_prototyping', name='about_prototyping'),
    url(r'^about/$', 'labman_ud.views.about', name='about'),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),

    # Login & Logout views
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login_view'),
    url(r'^logout/$', 'labman_ud.views.logout_view', name='logout_view'),

    # Entities urls
    url(r'^funding_programs/', include('entities.funding_programs.urls')),
    url(r'^news/', include('entities.news.urls')),
    url(r'^organizations/', include('entities.organizations.urls')),
    url(r'^people/', include('entities.persons.urls')),
    url(r'^projects/', include('entities.projects.urls')),
    url(r'^publications/', include('entities.publications.urls')),

    url(r'^management/', include('management.urls')),
    url(r'^populate_database/', 'labman_setup.views.populate_database', name='populate_database'),

    # Custom app urls
    url(r'^charts/', include('charts.urls')),
    # url(r'^semantic_search/', include('semantic_search.urls')),

    # Third-party app urls
    url(r'^redactor/', include('redactor.urls')),

    # Just for development purposes, serve in another way in production
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)

urlpatterns += staticfiles_urlpatterns()

handler404 = 'labman_ud.views.view404'
