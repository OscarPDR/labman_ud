
from django.conf.urls import url

urlpatterns = [
    url(r'^$', 'charts.views.chart_index', name='chart_index'),

    # /funding
    url(r'^funding/total_incomes/$', 'charts.views.funding_total_incomes', name='funding_total_incomes'),
    url(r'^funding/total_incomes_by_scope/$', 'charts.views.funding_total_incomes_by_scope', name='funding_total_incomes_by_scope'),
    url(r'^funding/incomes/(?P<year>\d{4})/(?P<scope>\S+)$', 'charts.views.funding_incomes_by_year_and_scope', name='funding_incomes_by_year_and_scope'),
    url(r'^funding/incomes/(?P<year>\d{4})$', 'charts.views.funding_incomes_by_year', name='funding_incomes_by_year'),
    url(r'^funding/incomes_by_project/$', 'charts.views.funding_incomes_by_project_index', name='funding_incomes_by_project_index'),
    url(r'^funding/incomes_by_project/(?P<project_slug>\S+)$', 'charts.views.funding_incomes_by_project', name='funding_incomes_by_project'),

    # /publications
    url(r'^publications/egonetwork/(?P<author_slug>\S+)$', 'charts.views.publications_egonetwork', name='publications_egonetwork'),
    url(r'^publications/total_number/(?P<author_slug>\S+)$', 'charts.views.publications_by_author', name='publications_by_author'),
    url(r'^publications/tags/(?P<author_slug>\S+)$', 'charts.views.tags_by_author', name='tags_by_author'),

    url(r'^publications/total_number/$', 'charts.views.publications_number_of_publications', name='publications_number_of_publications'),

    url(
        r'^publications/coauthorships/(?P<max_position>\d)/$',
        'charts.views.publication_coauthorships',
        name='publication_coauthorships_max_position',
    ),
    url(
        r'^publications/coauthorships/$',
        'charts.views.publication_coauthorships',
        name='publication_coauthorships',
    ),
    url(
        r'^publications/coauthorships_within_group/(?P<max_position>\d)/$',
        'charts.views.publication_coauthorships',
        {'within_group': True},
        name='publication_coauthorships_within_group_max_position',
    ),
    url(
        r'^publications/coauthorships_within_group/$',
        'charts.views.publication_coauthorships',
        {'within_group': True},
        name='publication_coauthorships_within_group',
    ),

    # /projects
    url(r'^projects/total_number/$', 'charts.views.projects_number_of_projects', name='projects_number_of_projects'),

    url(
        r'^projects/collaborations/exclude_leaders/$',
        'charts.views.project_collaborations',
        {'exclude_leaders': True},
        name='project_collaborations_exclude_leaders',
    ),
    url(
        r'^projects/collaborations/$',
        'charts.views.project_collaborations',
        name='project_collaborations',
    ),
    url(
        r'^projects/collaborations_within_group/exclude_leaders/$',
        'charts.views.project_collaborations',
        {'exclude_leaders': True, 'within_group': True},
        name='project_collaborations_within_group_exclude_leaders',
    ),
    url(
        r'^projects/collaborations_within_group/$',
        'charts.views.project_collaborations',
        {'within_group': True},
        name='project_collaborations_within_group',
    ),

    # /people
    url(r'^people/timeline/(?P<person_slug>\S+)$', 'charts.views.person_timeline', name='person_timeline'),
    url(r'^people/projects_timeline/(?P<person_slug>\S+)$', 'charts.views.projects_timeline', name='projects_timeline'),
    url(r'^people/timeline/$', 'charts.views.group_timeline', name='group_timeline'),
    url(r'^people/position_pie/$', 'charts.views.members_position_pie', name='position_pie'),
    url(r'^people/related/(?P<person_slug>\S+)/top-5/$', 'charts.views.related_persons', {'top': True}, name='related_persons_top'),
    url(r'^people/related/(?P<person_slug>\S+)/$', 'charts.views.related_persons', {'top': False}, name='related_persons'),
    url(r'^people/gender_distribution/(?P<organization_slug>\S+)/$', 'charts.views.gender_distribution', name='gender_distribution'),
    url(r'^people/gender_distribution/$', 'charts.views.gender_distribution', name='gender_distribution'),
    url(r'^people/position_distribution/(?P<organization_slug>\S+)/$', 'charts.views.position_distribution', name='position_distribution'),
    url(r'^people/position_distribution/$', 'charts.views.position_distribution', name='position_distribution'),
]
