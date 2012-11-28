from django.conf.urls import patterns, include, url

urlpatterns = patterns('',
    url(r'^$', 'employee_manager.views.home', name='home'),
    # (r'^organizaciones/', include('organization_manager.urls')),
    # (r'^personas/', include('employee_manager.urls')),
    # (r'^proyectos/', include('project_manager.urls')),
)
