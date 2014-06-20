from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',

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

    url(r'^publications/coauthorship/(?P<max_position>\d)$', 'charts.views.publications_coauthorship', name='publications_coauthorship_max_position'),
    url(r'^publications/coauthorship/$', 'charts.views.publications_coauthorship', name='publications_coauthorship'),
    url(r'^publications/morelab_coauthorship/(?P<max_position>\d)$', 'charts.views.publications_morelab_coauthorship', name='publications_morelab_coauthorship_max_position'),
    url(r'^publications/morelab_coauthorship/$', 'charts.views.publications_morelab_coauthorship', name='publications_morelab_coauthorship'),
    url(r'^publications/total_number/$', 'charts.views.publications_number_of_publications', name='publications_number_of_publications'),

    # /projects
    url(r'^projects/collaborations/$', 'charts.views.projects_collaborations', name='projects_collaborations'),
    url(r'^projects/morelab_collaborations/$', 'charts.views.projects_morelab_collaborations', name='projects_morelab_collaborations'),
    url(r'^projects/total_number/$', 'charts.views.projects_number_of_projects', name='projects_number_of_projects'),

    # /people
    url(r'^people/timeline/(?P<person_slug>\S+)$', 'charts.views.person_timeline', name='person_timeline'),
    url(r'^people/projects_timeline/(?P<person_slug>\S+)$', 'charts.views.projects_timeline', name='projects_timeline'),
    url(r'^people/timeline/$', 'charts.views.group_timeline', name='group_timeline'),
    url(r'^people/position_pie/$', 'charts.views.members_position_pie', name='position_pie'),
    url(r'^people/gender_distribution/(?P<organization_slug>\S+)/$', 'charts.views.gender_distribution', name='gender_distribution'),
    url(r'^people/gender_distribution/$', 'charts.views.gender_distribution', name='gender_distribution'),
)

urlpatterns += staticfiles_urlpatterns()
