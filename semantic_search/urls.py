from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'semantic_search.views.semantic_search', name = 'semantic_search'),
    url(r'^semantic_search/$', 'semantic_search.views.query', name = 'query'),
)

urlpatterns += staticfiles_urlpatterns()
