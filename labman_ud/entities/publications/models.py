# coding: utf-8

import os

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify


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


def thesis_path(self, filename):
    return "%s/%s/%s%s" % ("publications", "theses", self.slug, os.path.splitext(filename)[-1])


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
    # conferencePaper
    presented_at = models.ForeignKey(
        'events.Event',
        blank=True,
        null=True,
    )

    # REQUIRED
    publication_type = models.ForeignKey('PublicationType')

    # REQUIRED
    title = models.CharField(
        max_length=250,
    )

    # conferencePaper
    proceedings_title = models.CharField(
        max_length=250,
        blank=True,
        null=True,
    )

    # conferencePaper, journalArticle, bookSection, thesis
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

    # conferencePaper, journalArticle
    doi = models.CharField(
        max_length=100,
        verbose_name=u'DOI',
        blank=True,
        null=True,
    )

    pdf = models.FileField(
        upload_to=publication_path,
        blank=True,
        null=True,
    )

    language = models.ForeignKey(
        'utils.Language',
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

    year = models.PositiveIntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    volume = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    # conferencePaper, journalArticle, thesis, bookSection
    pages = models.CharField(
        max_length=25,
        blank=True,
        null=True,
    )

    # journalArticle
    issn = models.CharField(
        max_length=100,
        verbose_name=u'ISSN',
        blank=True,
        null=True,
    )

    # conferencePaper, bookSection
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
    tag = models.ForeignKey('utils.Tag')
    publication = models.ForeignKey('Publication')

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.publication.title, self.tag.tag)


#########################
# Model: PublicationAuthor
#########################

class PublicationAuthor(models.Model):
    author = models.ForeignKey('persons.Person')
    publication = models.ForeignKey('Publication')

    position = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s has written: %s' % (self.author.full_name, self.publication.title)


#########################
# Model: Thesis
#########################

class Thesis(models.Model):
    title = models.CharField(
        max_length=1000,
    )

    slug = models.SlugField(
        max_length=1000,
        blank=True,
        unique=True,
    )

    advisor = models.ForeignKey('persons.Person')
    co_advisors = models.ManyToManyField('persons.Person', through='CoAdvisor', related_name='advised_theses')

    registration_date = models.DateField(
        blank=True,
        null=True,
    )

    year = models.PositiveIntegerField()

    main_language = models.ForeignKey('utils.Language')

    abstract_en = models.TextField(
        max_length=2500,
        blank=True,
    )

    abstract_es = models.TextField(
        max_length=2500,
        blank=True,
    )

    # topics

    pdf = models.FileField(
        upload_to=thesis_path,
        blank=True,
        null=True,
    )

    viva = models.ForeignKey('events.Viva')

    phd_program = models.ForeignKey('utils.PhDProgram')

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.year = self.registration_date.year
        self.slug = slugify(str(self.title.encode('utf-8')))
        super(Thesis, self).save(*args, **kwargs)


#########################
# Model: CoAdvisor
#########################

class CoAdvisor(models.Model):
    thesis = models.ForeignKey('Thesis')
    co_advisor = models.ForeignKey('persons.Person')

    def __unicode__(self):
        return u'%s has co-advised the thesis: %s' % (self.co_advisor.full_name, self.thesis.title)


#########################
# Model: ThesisAuthor
#########################

class ThesisAuthor(models.Model):
    author = models.ForeignKey('persons.Person')
    thesis = models.ForeignKey('Thesis')

    def __unicode__(self):
        return u'%s has thesis: %s' % (self.author.full_name, self.thesis.title)
