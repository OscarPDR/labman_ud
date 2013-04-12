from django.conf.urls import patterns, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = patterns('',
    url(r'^$', 'semantic_search.views.semantic_search', name = 'semantic_search'),
    url(r'^embedded/$', 'semantic_search.views.semantic_searcher', name = 'semantic_searcher'),
)

urlpatterns += staticfiles_urlpatterns()
