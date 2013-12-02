# coding: utf-8

import requests
import tweetpony

from django.conf import settings
from django.db import models
from django.template.defaultfilters import slugify

from datetime import datetime
from redactor.fields import RedactorField


# Create your models here.


def post_tweet(obj):
    r = requests.get('%s%s%s' % (settings.KARMACRACY_URL, settings.NEWS_DETAIL_BASE_URL, obj.slug))

    short_link = r.text

    tweetpony_api = tweetpony.API(
        consumer_key=settings.TWEETPONY_CONSUMER_KEY,
        consumer_secret=settings.TWEETPONY_CONSUMER_SECRET,
        access_token=settings.TWEETPONY_ACCESS_TOKEN,
        access_token_secret=settings.TWEETPONY_ACCESS_TOKEN_SECRET
    )

    if len(obj.title) >= settings.NEWS_TITLE_MAX_LENGTH:
        tweet_title = '%s...' % (obj.title[:settings.NEWS_TITLE_MAX_LENGTH])
    else:
        tweet_title = obj.title

    tweet = '%s: %s' % (tweet_title, short_link)

    print tweet

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

    content = RedactorField()

    created = models.DateTimeField(default=datetime.now, blank=True)

    tags = models.ManyToManyField('utils.Tag', through='NewsTag', related_name='news')
    projects = models.ManyToManyField('projects.Project', through='ProjectRelatedToNews', related_name='news')
    publications = models.ManyToManyField('publications.Publication', through='PublicationRelatedToNews', related_name='news')
    persons = models.ManyToManyField('persons.Person', through='PersonRelatedToNews', related_name='news')

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title.encode('utf-8')))

        #post_tweet(self)

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
