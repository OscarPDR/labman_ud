from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'employee_manager.views.index', name = 'index'),
    url(r'^add/$', 'employee_manager.views.add_employee', name = 'add_employee'),
    url(r'^eliminar/(\d*)$', 'employee_manager.views.delete_employee', name = 'delete_employee'),
    # (r'^organizaciones/', include('organization_manager.urls')),
    # (r'^personas/', include('employee_manager.urls')),
    # (r'^proyectos/', include('project_manager.urls')),
)

urlpatterns += staticfiles_urlpatterns()
