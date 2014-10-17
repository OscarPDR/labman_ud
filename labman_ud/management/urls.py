
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'management.views.check_names_similarity', name='check_names_similarity_default'),
    url(r'^ratio/(?P<threshold_ratio>\d{2})/$', 'management.views.check_names_similarity', name='check_names_similarity'),
    url(r'^alias/(?P<person_id>\d+)/(?P<alias_id>\d+)/$', 'management.views.assign_alias', name='assign_alias'),
]
