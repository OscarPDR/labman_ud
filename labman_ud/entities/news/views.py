# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from entities.news.models import News


# Create your views here.


#########################
# View: news_index
#########################

def news_index(request):
    news = News.objects.all().order_by('-created')

    return render_to_response('news/index.html', {
            'news': news,
        },
        context_instance=RequestContext(request))


#########################
# View: view_news
#########################

def view_news(request, news_slug):
    news = News.objects.get(slug=news_slug)
    # tags = news.tags.all()

    return render_to_response('news/info.html', {
            'news': news,
            # 'tags': tags,
        },
        context_instance=RequestContext(request))
