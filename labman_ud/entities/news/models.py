
from django.db import models
from django.template.defaultfilters import slugify

from datetime import datetime
from redactor.fields import RedactorField

from management.post_tweet import post_tweet


###     News
####################################################################################################

class News(models.Model):

    post_tweet = models.BooleanField(
        default=False,
    )

    tweet_cc = models.CharField(
        max_length=70,
        blank=True,
        null=True,
    )

    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    content = RedactorField()

    created = models.DateTimeField(
        default=datetime.now,
        blank=True,
        null=True,
    )

    city = models.ForeignKey(
        'utils.City',
        blank=True,
        null=True,
    )

    country = models.ForeignKey(
        'utils.Country',
        blank=True,
        null=True,
    )

    tags = models.ManyToManyField(
        'utils.Tag',
        through='NewsTag',
        related_name='news',
    )

    projects = models.ManyToManyField(
        'projects.Project',
        through='ProjectRelatedToNews',
        related_name='news',
    )

    publications = models.ManyToManyField(
        'publications.Publication',
        through='PublicationRelatedToNews',
        related_name='news',
    )

    persons = models.ManyToManyField(
        'persons.Person',
        through='PersonRelatedToNews',
        related_name='news',
    )

    class Meta:
        ordering = ('-created',)
        verbose_name = u'News piece'
        verbose_name_plural = u'News pieces'

    def __unicode__(self):
        return u'%s' % self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)

        if self.post_tweet:
            post_tweet(self)

        self.content = self.content.replace("<img src=", "<img class='img-responsive' src=")

        super(News, self).save(*args, **kwargs)


###     NewsTag
####################################################################################################

class NewsTag(models.Model):

    tag = models.ForeignKey('utils.Tag')

    news = models.ForeignKey('News')

    class Meta:
        verbose_name = u'News Tag'
        verbose_name_plural = u'News Tags'


###     ProjectRelatedToNews
####################################################################################################

class ProjectRelatedToNews(models.Model):

    project = models.ForeignKey('projects.Project')

    news = models.ForeignKey('News')

    class Meta:
        verbose_name = u'Project related to News piece'
        verbose_name_plural = u'Projects related to News pieces'


###     PublicationRelatedToNews
####################################################################################################

class PublicationRelatedToNews(models.Model):

    publication = models.ForeignKey('publications.Publication')

    news = models.ForeignKey('News')

    class Meta:
        verbose_name = u'Publication related to News piece'
        verbose_name_plural = u'Publications related to News pieces'


###     PersonRelatedToNews
####################################################################################################

class PersonRelatedToNews(models.Model):

    person = models.ForeignKey('persons.Person')

    news = models.ForeignKey('News')

    class Meta:
        verbose_name = u'Person related to News piece'
        verbose_name_plural = u'People related to News pieces'


###     EventRelatedToNews
####################################################################################################

class EventRelatedToNews(models.Model):

    event = models.ForeignKey('events.Event')

    news = models.ForeignKey('News')

    class Meta:
        verbose_name = u'Event related to News piece'
        verbose_name_plural = u'Events related to News pieces'
