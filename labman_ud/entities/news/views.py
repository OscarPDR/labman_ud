# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from entities.news.models import News, PersonRelatedToNews, ProjectRelatedToNews, PublicationRelatedToNews

from entities.persons.models import Person

from entities.projects.models import Project

from entities.publications.models import Publication


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

    related_persons_ids = PersonRelatedToNews.objects.filter(news=news.id).values('person_id')
    related_persons = Person.objects.filter(id__in=related_persons_ids).order_by('slug')

    related_projects_ids = ProjectRelatedToNews.objects.filter(news=news.id).values('project_id')
    related_projects = Project.objects.filter(id__in=related_projects_ids).order_by('slug')

    related_publications_ids = PublicationRelatedToNews.objects.filter(news=news.id).values('publication_id')
    related_publications = Publication.objects.filter(id__in=related_publications_ids).order_by('slug')

    return render_to_response('news/info.html', {
            'news': news,
            # 'tags': tags,
            'related_persons': related_persons,
            'related_projects': related_projects,
            'related_publications': related_publications,
        },
        context_instance=RequestContext(request))
