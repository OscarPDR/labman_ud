from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'employee_manager.views.index', name = 'employee_index'),
    url(r'^nueva/$', 'employee_manager.views.add_employee', name = 'add_employee'),
    url(r'^editar/(\S+)$', 'employee_manager.views.edit_employee', name = 'edit_employee'),
    url(r'^eliminar/(\S+)$', 'employee_manager.views.delete_employee', name = 'delete_employee'),
)

urlpatterns += staticfiles_urlpatterns()
