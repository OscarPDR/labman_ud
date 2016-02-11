
from django.conf.urls import url

import entities.funding_programs.views as views

urlpatterns = [
    url(r'^$', views.funding_program_index, name='funding_program_index'),
    url(r'^info/(?P<funding_program_slug>\S+)/$', views.funding_program_info, name='funding_program_info'),
]
