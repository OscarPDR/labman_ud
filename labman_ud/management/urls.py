
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'management.views.index', name='management_index'),
    url(r'^similarity_ratio/(?P<threshold_ratio>\d{2})/$', 'management.views.check_names_similarity', name='check_names_similarity'),
    url(r'^similarity_ratio/default/$', 'management.views.check_names_similarity', name='check_names_similarity_default'),
    url(r'^alias/(?P<person_id>\d+)/(?P<alias_id>\d+)/(?P<threshold_ratio>\d{2})/$', 'management.views.assign_alias', name='assign_alias'),
    url(r'^ignore_relationship/(?P<test_person_id>\d+)/(?P<testing_person_id>\d+)/(?P<threshold_ratio>\d{2})/$', 'management.views.ignore_relationship', name='ignore_relationship'),
    url(r'^reset_ignored_relationships/(?P<threshold_ratio>\d{2})/$', 'management.views.reset_ignored_relationships', name='reset_ignored_relationships'),
    url(r'^display_tags/$', 'management.views.manage_tags', name='manage_tags'),
    url(r'^rename_tag/(?P<tag_id>\d+)/$', 'management.views.rename_tag', name='rename_tag'),
    url(r'^parse_publications/$', 'management.views.parse_publications', name='parse_publications'),
    url(r'^reset/$', 'management.views.synchronize_publications', name='reset_publications'),
    url(r'^synchronize/(?P<from_version>\d+)/$', 'management.views.synchronize_publications', name='synchronize_publications'),
]
