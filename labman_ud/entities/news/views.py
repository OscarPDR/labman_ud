# coding: utf-8

from collections import OrderedDict

from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import News, PersonRelatedToNews, ProjectRelatedToNews, PublicationRelatedToNews

from entities.persons.models import Person
from entities.projects.models import Project
from entities.publications.models import Publication


# Create your views here.


###########################################################################
# View: news_index
###########################################################################

def news_index(request):
    _news = News.objects.all().order_by('-created')

    news = OrderedDict()

    for news_piece in _news:
        year_month = u'%s %s' % (news_piece.created.strftime('%B'), news_piece.created.year)
        if not year_month in news:
            news[year_month] = []
        news[year_month].append(news_piece)

    # dictionary to be returned in render_to_response()
    return_dict = {
        'news': news,
    }

    return render_to_response('news/index.html', return_dict, context_instance=RequestContext(request))


###########################################################################
# View: view_news
###########################################################################

def view_news(request, news_slug):
    news = News.objects.get(slug=news_slug)
    # tags = news.tags.all()

    related_persons_ids = PersonRelatedToNews.objects.filter(news=news.id).values('person_id')
    related_persons = Person.objects.filter(id__in=related_persons_ids).order_by('slug')

    related_projects_ids = ProjectRelatedToNews.objects.filter(news=news.id).values('project_id')
    related_projects = Project.objects.filter(id__in=related_projects_ids).order_by('slug')

    related_publications_ids = PublicationRelatedToNews.objects.filter(news=news.id).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).order_by('slug')

    if not related_persons and not related_projects and not related_publications:
        related = False
    else:
        related = True

    # dictionary to be returned in render_to_response()
    return_dict = {
        # 'tags': tags,
        'news': news,
        'related': related,
        'related_persons': related_persons,
        'related_projects': related_projects,
        'related_publications': related_publications,
    }

    return render_to_response('news/info.html', return_dict, context_instance=RequestContext(request))
