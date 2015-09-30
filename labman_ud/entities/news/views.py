# -*- encoding: utf-8 -*-

import threading
import weakref

from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404
from django.contrib.syndication.views import Feed

from .models import News

from labman_setup.models import LabmanDeployGeneralSettings


###     news_index()
####################################################################################################

def news_index(request):

    news = News.objects.all().order_by('-created', 'title')

    # dictionary to be returned in render(request, )
    return_dict = {
        'news': news,
        'web_title': 'News',
    }

    return render(request, 'news/index.html', return_dict)


###     view_news(news_slug)
####################################################################################################

def view_news(request, news_slug):

    news_pieces = News.objects.prefetch_related('projects', 'publications', 'persons')
    news_piece = get_object_or_404(news_pieces, slug=news_slug)

    num_rel_projects = len(news_piece.projects.related_val)
    num_rel_publications = len(news_piece.publications.related_val)
    num_rel_persons = len(news_piece.persons.related_val)

    # dictionary to be returned in render(request, )
    return_dict = {
        'has_related': bool(num_rel_projects or num_rel_publications or num_rel_persons),
        'news_piece': news_piece,
        'web_title': news_piece.title,
    }

    return render(request, 'news/info.html', return_dict)


###     LatestNewsFeed(Feed)
####################################################################################################

class LatestNewsFeed(Feed):
    def __init__(self, *args, **kwargs):
        super(LatestNewsFeed, self).__init__(*args, **kwargs)
        self.__request = threading.local()

    try:
        _settings = LabmanDeployGeneralSettings.objects.get()
        research_group_short_name = _settings.research_group_short_name

    except:
        research_group_short_name = u'Our'

    title = u'%s news' % research_group_short_name
    description = u'%s news' % research_group_short_name

    def get_object(self, request):
        self.__request.request = weakref.proxy(request)
        return super(LatestNewsFeed, self).get_object(request)

    def link(self, obj):
        url = reverse('news_index')
        return self.__request.request.build_absolute_uri(url)

    def items(self):
        return News.objects.order_by('-created')[:30]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.content

    def item_link(self, item):
        url = reverse('view_news', args=[item.slug])
        return self.__request.request.build_absolute_uri(url)
