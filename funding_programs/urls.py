from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'funding_programs.views.funding_program_index', name = 'funding_program_index'),
    url(r'^info/(\S+)$', 'funding_programs.views.funding_program_info', name = 'funding_program_info'),
)

urlpatterns += staticfiles_urlpatterns()
