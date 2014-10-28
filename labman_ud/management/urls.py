
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'management.views.index', name='management_index'),
    url(r'^similarity_ratio/(?P<threshold_ratio>\d{2})/$', 'management.views.check_names_similarity', name='check_names_similarity'),
    url(r'^similarity_ratio/default/$', 'management.views.check_names_similarity', name='check_names_similarity_default'),
    url(r'^alias/(?P<person_id>\d+)/(?P<alias_id>\d+)/(?P<threshold_ratio>\d{2})/$', 'management.views.assign_alias', name='assign_alias'),
    url(r'^ignore_relationship/(?P<test_person_id>\d+)/(?P<testing_person_id>\d+)/(?P<threshold_ratio>\d{2})/$', 'management.views.ignore_relationship', name='ignore_relationship'),
    url(r'^reset_ignored_relationships/(?P<threshold_ratio>\d{2})/$', 'management.views.reset_ignored_relationships', name='reset_ignored_relationships'),
    url(r'^tags/$', 'management.views.tags', name='tags'),
]
