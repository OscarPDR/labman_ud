from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'employees.views.employee_index', name = 'employee_index'),
    url(r'^add/$', 'employees.views.add_employee', name = 'add_employee'),
    url(r'^info/(\S+)$', 'employees.views.employee_info', name = 'employee_info'),
    url(r'^edit/(\S+)$', 'employees.views.edit_employee', name = 'edit_employee'),
    url(r'^delete/(?P<slug>\S+)$', 'employees.views.delete_employee', name = 'delete_employee'),
)

urlpatterns += staticfiles_urlpatterns()
