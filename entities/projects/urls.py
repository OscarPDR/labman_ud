from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'entities.projects.views.project_index', name = 'project_index'),
    url(r'^info/(\S+)$', 'entities.projects.views.project_info', name = 'project_info'),
    url(r'^email/(\S+)$', 'entities.projects.views.email_project', name = 'email_project'),
)

urlpatterns += staticfiles_urlpatterns()
