from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',

    url(r'^$', 'charts.views.chart_index', name='chart_index'),

    # /funding
    url(r'^funding/$', 'charts.views.funding_charts_index', name='funding_charts_index'),
    
    url(r'^funding/total_incomes/$', 'charts.views.funding_total_incomes', name='funding_total_incomes'),
    url(r'^funding/total_incomes_by_scope/$', 'charts.views.funding_total_incomes_by_scope', name='funding_total_incomes_by_scope'),
    url(r'^funding/incomes/(?P<year>\d{4})/(?P<scope>\S+)$', 'charts.views.funding_incomes_by_year_and_scope', name='funding_incomes_by_year_and_scope'),
    url(r'^funding/incomes/(?P<year>\d{4})$', 'charts.views.funding_incomes_by_year', name='funding_incomes_by_year'),
    url(r'^funding/incomes_by_project/$', 'charts.views.funding_incomes_by_project_index', name='funding_incomes_by_project_index'),
    url(r'^funding/incomes_by_project/(?P<project_slug>\S+)$', 'charts.views.funding_incomes_by_project', name='funding_incomes_by_project'),

    # /publications
    url(r'^publications/$', 'charts.views.publications_charts_index', name='publications_charts_index'),
    
    url(r'^publications/coauthorship/$', 'charts.views.publications_coauthorship', name='publications_coauthorship'),
    url(r'^publications/morelab_coauthorship/$', 'charts.views.publications_morelab_coauthorship', name='publications_morelab_coauthorship'),
    url(r'^publications/total_number/$', 'charts.views.publications_number_of_publications', name='publications_number_of_publications'),

    # /projects
    url(r'^projects/$', 'charts.views.projects_charts_index', name='projects_charts_index'),
    
    url(r'^projects/coauthorship/$', 'charts.views.projects_coauthorship', name='projects_coauthorship'),
    
)

urlpatterns += staticfiles_urlpatterns()
