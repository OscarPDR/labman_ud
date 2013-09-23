# coding: utf-8

import bitly_api
import tweetpony

from django.db import models
from django.template.defaultfilters import slugify
from django.conf import settings

from ckeditor.fields import RichTextField


# Create your models here.


NEWS_DETAIL_BASE_URL = 'http://dev.morelab.deusto.es/labman_ud/news/view/'
NEWS_TITLE_MAX_LENGTH = 100


def post_tweet(obj):
    bitly = bitly_api.Connection(access_token=settings.BITLY_ACCESS_TOKEN)

    long_url = '%s%s' % (NEWS_DETAIL_BASE_URL, obj.slug)
    short_link = bitly.shorten(long_url)

    tweetpony_api = tweetpony.API(
        consumer_key=settings.TWEETPONY_CONSUMER_KEY,
        consumer_secret=settings.TWEETPONY_CONSUMER_SECRET,
        access_token=settings.TWEETPONY_ACCESS_TOKEN,
        access_token_secret=settings.TWEETPONY_ACCESS_TOKEN_SECRET
    )

    if len(obj.title) >= NEWS_TITLE_MAX_LENGTH:
        tweet_title = '%s...' % (obj.title[:NEWS_TITLE_MAX_LENGTH])
    else:
        tweet_title = obj.title

    tweet = '%s: %s' % (tweet_title, short_link['url'])

    try:
        tweetpony_api.update_status(status=tweet)
    except tweetpony.APIError as err:
        print "Oops, something went wrong! Twitter returned error #%i and said: %s" % (err.code, err.description)


#########################
# Model: New
#########################

class News(models.Model):
    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    content = RichTextField()

    created = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField('utils.Tag', through='NewsTag', related_name='news')
    projects = models.ManyToManyField('projects.Project', through='ProjectRelatedToNews', related_name='news')
    publications = models.ManyToManyField('publications.Publication', through='PublicationRelatedToNews', related_name='news')
    persons = models.ManyToManyField('persons.Person', through='PersonRelatedToNews', related_name='news')

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title.encode('utf-8')))

        # post_tweet(self)

        super(News, self).save(*args, **kwargs)


#########################
# Model: NewsTag
#########################

class NewsTag(models.Model):
    tag = models.ForeignKey('utils.Tag')
    news = models.ForeignKey('News')

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.news.title, self.tag.name)


#########################
# Model: ProjectRelatedToNews
#########################

class ProjectRelatedToNews(models.Model):
    project = models.ForeignKey('projects.Project')
    news = models.ForeignKey('News')

    def __unicode__(self):
        return u'%s refers to project: %s' % (self.news.title, self.project.short_name)


#########################
# Model: PublicationRelatedToNews
#########################

class PublicationRelatedToNews(models.Model):
    publication = models.ForeignKey('publications.Publication')
    news = models.ForeignKey('News')

    def __unicode__(self):
        return u'%s refers to project: %s' % (self.news.title, self.publication.title)


#########################
# Model: PersonRelatedToNews
#########################

class PersonRelatedToNews(models.Model):
    person = models.ForeignKey('persons.Person')
    news = models.ForeignKey('News')

    def __unicode__(self):
        return u'%s refers to project: %s' % (self.news.title, self.person.full_name)
