
from django.conf.urls import url

import charts.views as views

urlpatterns = [
    url(r'^$', views.chart_index, name='chart_index'),

    ### topic_clouds
    ###########################################################################

    url(r'^topics/(?P<entity_slug>\S+)/(?P<person_slug>\S+)/$', views.topic_cloud, name='topics_by_person'),
    url(r'^topics/(?P<entity_slug>\S+)/$', views.topic_cloud, name='topics_by_entity'),

    # /funding
    url(r'^funding/total_incomes/$', views.funding_total_incomes, name='funding_total_incomes'),
    url(r'^funding/total_incomes_by_scope/$', views.funding_total_incomes_by_scope, name='funding_total_incomes_by_scope'),
    url(r'^funding/incomes/(?P<year>\d{4})/(?P<scope>\S+)$', views.funding_incomes_by_year_and_scope, name='funding_incomes_by_year_and_scope'),
    url(r'^funding/incomes/(?P<year>\d{4})$', views.funding_incomes_by_year, name='funding_incomes_by_year'),
    url(r'^funding/incomes_by_project/$', views.funding_incomes_by_project_index, name='funding_incomes_by_project_index'),
    url(r'^funding/incomes_by_project/(?P<project_slug>\S+)$', views.funding_incomes_by_project, name='funding_incomes_by_project'),

    # /publications
    url(r'^publications/egonetwork/(?P<author_slug>\S+)$', views.publications_egonetwork, name='publications_egonetwork'),
    url(r'^publications/total_number/(?P<author_slug>\S+)$', views.publications_by_author, name='publications_by_author'),
    url(r'^publications/by_place/(?P<author_slug>\S+)/(?P<child_type>\S+)$', views.publication_places_by_author, name='publication_places_by_author_and_type'),
    url(r'^publications/by_place/(?P<author_slug>\S+)$', views.publication_places_by_author, name='publication_places_by_author'),

    url(r'^publications/total_number/$', views.publications_number_of_publications, name='publications_number_of_publications'),

    url(r'^publications/coauthorships/(?P<max_position>\d)/$', views.publication_coauthorships, name='publication_coauthorships_max_position'),
    url(r'^publications/coauthorships/$', views.publication_coauthorships, name='publication_coauthorships'),
    url(r'^publications/coauthorships_within_group/(?P<max_position>\d)/$', views.publication_coauthorships, {'within_group': True}, name='publication_coauthorships_within_group_max_position'),
    url(r'^publications/coauthorships_within_group/$', views.publication_coauthorships, {'within_group': True}, name='publication_coauthorships_within_group'),

    # /projects
    url(r'^projects/total_number/$', views.projects_number_of_projects, name='projects_number_of_projects'),

    url(r'^projects/collaborations/exclude_leaders/$', views.project_collaborations, {'exclude_leaders': True}, name='project_collaborations_exclude_leaders'),
    url(r'^projects/collaborations/$', views.project_collaborations, name='project_collaborations'),
    url(r'^projects/collaborations_within_group/exclude_leaders/$', views.project_collaborations, {'exclude_leaders': True, 'within_group': True}, name='project_collaborations_within_group_exclude_leaders'),
    url(r'^projects/collaborations_within_group/$', views.project_collaborations, {'within_group': True}, name='project_collaborations_within_group'),

    # /people
    url(r'^people/timeline/(?P<person_slug>\S+)$', views.person_timeline, name='person_timeline'),
    url(r'^people/projects_timeline/(?P<person_slug>\S+)$', views.projects_timeline, name='projects_timeline'),
    url(r'^people/timeline/$', views.group_timeline, name='group_timeline'),
    url(r'^people/position_pie/$', views.members_position_pie, name='position_pie'),
    url(r'^people/related/(?P<person_slug>\S+)/top-5/$', views.related_persons, {'top': True}, name='related_persons_top'),
    url(r'^people/related/(?P<person_slug>\S+)/$', views.related_persons, {'top': False}, name='related_persons'),
    url(r'^people/gender_distribution/(?P<organization_slug>\S+)/$', views.gender_distribution, name='gender_distribution'),
    url(r'^people/gender_distribution/$', views.gender_distribution, name='gender_distribution'),
    url(r'^people/position_distribution/(?P<organization_slug>\S+)/$', views.position_distribution, name='position_distribution'),
    url(r'^people/position_distribution/$', views.position_distribution, name='position_distribution'),
]
