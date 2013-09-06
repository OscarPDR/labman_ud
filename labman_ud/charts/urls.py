from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^total_incomes/$', 'charts.views.total_incomes', name='total_incomes'),
    url(r'^total_incomes_by_scope/$', 'charts.views.total_incomes_by_scope', name='total_incomes_by_scope'),
    url(r'^incomes/(?P<year>\d{4})/(?P<scope>\S+)$', 'charts.views.incomes_by_year_and_scope', name='incomes_by_year_and_scope'),
    url(r'^incomes/(?P<year>\d{4})$', 'charts.views.incomes_by_year', name='incomes_by_year'),
    url(r'^incomes_by_project/$', 'charts.views.incomes_by_project_index', name='incomes_by_project_index'),
    url(r'^incomes_by_project/(?P<project_slug>\S+)$', 'charts.views.incomes_by_project', name='incomes_by_project'),

    url(r'^number_of_publications/$', 'charts.views.number_of_publications', name='number_of_publications'),
)

urlpatterns += staticfiles_urlpatterns()
