from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'funding_programs.views.funding_program_index', name = 'funding_program_index'),
    url(r'^add/$', 'funding_programs.views.add_funding_program', name = 'add_funding_program'),
    url(r'^info/(\S+)$', 'funding_programs.views.funding_program_info', name = 'funding_program_info'),
    url(r'^edit/(\S+)$', 'funding_programs.views.edit_funding_program', name = 'edit_funding_program'),
    url(r'^delete/(\S+)$', 'funding_programs.views.delete_funding_program', name = 'delete_funding_program'),
)

urlpatterns += staticfiles_urlpatterns()
