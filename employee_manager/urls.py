from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'employee_manager.views.index', name = 'index'),
    # (r'^organizaciones/', include('organization_manager.urls')),
    # (r'^personas/', include('employee_manager.urls')),
    # (r'^proyectos/', include('project_manager.urls')),
)
