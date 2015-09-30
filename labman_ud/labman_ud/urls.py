
from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sites.models import Site

from .forms import LoginForm

admin.site.site_header = u'labman'
admin.site.unregister(Site)

urlpatterns = [
    url(r'^$', 'labman_ud.views.home', name='home'),
    url(r'^admin/', include(admin.site.urls)),

    # Login & Logout views
    url(r'login/$', 'django.contrib.auth.views.login', {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='login_view'),
    url(r'^logout/$', 'labman_ud.views.logout_view', name='logout_view'),

    url(r'^about/(?P<about_page_slug>\S+)/$', 'labman_ud.views.about_info', name='about_info'),

    # Entities urls
    url(r'^funding_programs/', include('entities.funding_programs.urls')),
    url(r'^news/', include('entities.news.urls')),
    url(r'^organizations/', include('entities.organizations.urls')),
    url(r'^people/', include('entities.persons.urls')),
    url(r'^p/(?P<person_slug>\S+)/$', 'entities.persons.views.member_info', name='full_url_member_info'),
    url(r'^p/$', 'entities.persons.views.members_redirect', name='members_redirect'),
    url(r'^projects/', include('entities.projects.urls')),
    url(r'^publications/', include('entities.publications.urls')),

    # Custom app urls
    url(r'^charts/', include('charts.urls')),
    url(r'^management/', include('management.urls')),
    url(r'^populate_database/', 'labman_setup.views.populate_database', name='populate_database'),

    # Third-party app urls
    url(r'^redactor/', include('redactor.urls')),

    # Just for development purposes, serve in another way in production
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
]

handler404 = 'labman_ud.views.view404'
