# coding: utf-8

import os

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

from entities.events.models import Event

from entities.persons.models import Person

from entities.utils.models import Tag, Language

from entities.organizations.models import Organization


# Create your models here.

MIN_YEAR_LIMIT = 2000
MAX_YEAR_LIMIT = 2030


def publication_path(self, filename):
    # if the publication is presented at any event (conference, workshop, etc.), it will be stored like:
    #   publications/2012/ucami/title-of-the-paper.pdf
    if self.presented_at:
        sub_folder = self.presented_at.slug

    # otherwise, it will be stored like:
    #   publications/2012/book-chapter/title-of-the-paper.pdf
    else:
        sub_folder = self.publication_type.slug

    return "%s/%s/%s/%s%s" % ("publications", self.year, sub_folder, self.slug, os.path.splitext(filename)[-1])


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
        null=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(PublicationType, self).save(*args, **kwargs)


#########################
# Model: Publication
#########################

class Publication(models.Model):
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

    proceedings_title = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    short_title = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    # REQUIRED
    abstract = models.TextField(
        max_length=5000,
    )

    doi = models.CharField(
        max_length=100,
        verbose_name=u'DOI',
        blank=True,
        null=True,
    )

    pdf = models.FileField(
        max_length=1000,
        upload_to=publication_path,
        blank=True,
        null=True,
    )

    language = models.ForeignKey(
        Language,
        null=True,
    )

    journal_abbreviation = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    published = models.DateField(
        blank=True,
        null=True,
    )

    year = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    volume = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    pages = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )

    issn = models.CharField(
        max_length=100,
        verbose_name=u'ISSN',
        blank=True,
        null=True,
    )

    isbn = models.CharField(
        max_length=100,
        verbose_name=u'ISBN',
        blank=True,
        null=True,
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
        null=True,
    )

    series_number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    series = models.CharField(
        max_length=300,
        blank=True,
        null=True,
    )

    edition = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    book_title = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    publisher = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    university = models.ForeignKey(Organization, blank=True, null=True)

    issue = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    series_text = models.TextField(
        max_length=500,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']

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
        return u'%s has written: %s' % (self.author.full_name, self.publication.title)
