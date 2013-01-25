from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'project_manager.views.project_index', name = 'project_index'),
    url(r'^add/$', 'project_manager.views.add_project', name = 'add_project'),
    url(r'^info/(\S+)$', 'project_manager.views.info_project', name = 'info_project'),
    url(r'^email/(\S+)$', 'project_manager.views.email_project', name = 'email_project'),
    url(r'^edit/(\S+)$', 'project_manager.views.edit_project', name = 'edit_project'),
    url(r'^delete/(\S+)$', 'project_manager.views.delete_project', name = 'delete_project'),
)

urlpatterns += staticfiles_urlpatterns()
