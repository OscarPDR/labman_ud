
from django.conf.urls import url


urlpatterns = [
    url(r'^$', 'entities.funding_programs.views.funding_program_index', name='funding_program_index'),
    url(r'^info/(?P<funding_program_slug>\S+)/$', 'entities.funding_programs.views.funding_program_info', name='funding_program_info'),
]
