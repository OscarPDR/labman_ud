# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify

from entities.events.models import Event

from entities.persons.models import Person

from entities.utils.models import Tag


# Create your models here.


def publication_path(self, filename):
    # if the publication is presented at any event (conference, workshop, etc.), it will be stored like:
    #   publications/2012/ucami/title-of-the-paper.pdf
    if self.presented_at:
        year = self.presented_at.year
        sub_folder = self.presented_at.slug

    # otherwise, it will be stored like:
    #   publications/2012/book-chapter/title-of-the-paper.pdf
    else:
        year = self.year
        sub_folder = self.publication_type.slug

    return "%s/%s/%s/%s%s" % ("publications", year, sub_folder, self.slug, os.path.splitext(filename)[-1])


#########################
# Model: PublicationType
#########################

class PublicationType(models.Model):
    name = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(PublicationType, self).save(*args, **kwargs)


#########################
# Model: Publication
#########################

class Publication(models.Model):
    # conferencePaper
    presented_at = models.ForeignKey(
        Event,
        blank=True,
        null=True,
    )

    # REQUIRED
    publication_type = models.ForeignKey(PublicationType)

    # REQUIRED
    title = models.CharField(
        max_length=250,
    )

    # conferencePaper
    proceedings_title = models.CharField(
        max_length=250,
    )

    # conferencePaper, journalArticle, bookSection, thesis
    short_title = models.CharField(
        max_length=150,
        blank=True,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    abstract = models.TextField(
        max_length=5000,
        blank=True,
    )

    # conferencePaper, journalArticle
    doi = models.CharField(
        max_length=100,
        verbose_name=u'DOI',
        blank=True,
    )

    pdf = models.FileField(
        upload_to=publication_path,
        blank=True,
        null=True,
    )

    language = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )

    # journalArticle
    journal_abbreviation = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    published = models.DateField(
        blank=True,
        null=True,
    )

    number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    volume = models.PositiveIntegerField(
        default=1,
        blank=True,
    )

    # conferencePaper, journalArticle, thesis, bookSection
    pages = models.CharField(
        max_length=25,
        blank=True,
    )

    # journalArticle
    issn = models.CharField(
        max_length=100,
        verbose_name=u'ISSN',
        blank=True,
    )

    # conferencePaper, bookSection
    isbn = models.CharField(
        max_length=100,
        verbose_name=u'ISBN',
        blank=True,
    )

    impact_factor = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        blank=True,
        null=True,
    )

    observations = models.TextField(
        max_length=3000,
        blank=True,
    )

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title.encode('utf-8')))

        super(Publication, self).save(*args, **kwargs)


#########################
# Model: PublicationTag
#########################

class PublicationTag(models.Model):
    tag = models.ForeignKey(Tag)
    publication = models.ForeignKey(Publication)

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.publication.title, self.tag.tag)


#########################
# Model: PublicationAuthor
#########################

class PublicationAuthor(models.Model):
    author = models.ForeignKey(Person)
    publication = models.ForeignKey(Publication)

    position = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.publication.title, self.tag.tag)
