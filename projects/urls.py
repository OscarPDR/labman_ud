from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'projects.views.project_index', name = 'project_index'),
    url(r'^info/(\S+)$', 'projects.views.project_info', name = 'project_info'),
    url(r'^email/(\S+)$', 'projects.views.email_project', name = 'email_project'),
)

urlpatterns += staticfiles_urlpatterns()
