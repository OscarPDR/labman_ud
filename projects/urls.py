from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'projects.views.project_index', name = 'project_index'),
    url(r'^add/$', 'projects.views.add_project', name = 'add_project'),
    url(r'^info/(\S+)$', 'projects.views.project_info', name = 'project_info'),
    url(r'^email/(\S+)$', 'projects.views.email_project', name = 'email_project'),
    url(r'^edit/(\S+)$', 'projects.views.edit_project', name = 'edit_project'),
    url(r'^delete/(\S+)$', 'projects.views.delete_project', name = 'delete_project'),

    url(r'^delete_employee/(?P<employee_slug>\S+)/from/(?P<project_slug>\S+)$', 'projects.views.delete_employee_from_project', name = 'delete_employee_from_project'),
    url(r'^delete_organization/(?P<organization_slug>\S+)/from/(?P<project_slug>\S+)$', 'projects.views.delete_organization_from_project', name = 'delete_organization_from_project'),
)

urlpatterns += staticfiles_urlpatterns()
