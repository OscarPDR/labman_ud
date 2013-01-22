from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'employee_manager.views.employee_index', name = 'employee_index'),
    url(r'^add/$', 'employee_manager.views.add_employee', name = 'add_employee'),
    url(r'^info/(\S+)$', 'employee_manager.views.info_employee', name = 'info_employee'),
    url(r'^edit/(\S+)$', 'employee_manager.views.edit_employee', name = 'edit_employee'),
    url(r'^delete/(\S+)$', 'employee_manager.views.delete_employee', name = 'delete_employee'),
)

urlpatterns += staticfiles_urlpatterns()
