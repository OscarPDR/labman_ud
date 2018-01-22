
from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


import entities.datasets.views as views

urlpatterns = [
    url(r'^$', views.datasets_index, name='datasets_index'),
    url(r'^filtered/$', views.datasets_index, name='filtered_dataset_query'),
    # url(r'^info/(?P<dataset_slug>\S+)/extended_information/$', views.dataset_ext_info, name='datasets_ext_info'),
    url(r'^info/(?P<dataset_slug>\S+)/$', views.dataset_info, name='datasets_info'),
    url(r'^tag/(?P<tag_slug>\S+)/$', views.datasets_index, name='datasets_tag'),
]

urlpatterns += staticfiles_urlpatterns()
