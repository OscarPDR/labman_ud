# coding: utf-8

from django.db import models
from django.template.defaultfilters import slugify

from events.models import Event


# Create your models here.


#########################
# Model: PublicationType
#########################

class PublicationType(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=u'Name',
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    def __unicode__(self):
        return u'%s' % (self.name)


#########################
# Model: Publication
#########################

class Publication(models.Model):
    presented_at = models.ForeignKey(Event)

    publication_type = models.ForeignKey(PublicationType)

    title = models.CharField(
        max_length=250,
        verbose_name=u'Title *',    # Required
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
    )

    abstract = models.TextField(
        max_length=5000,
        verbose_name=u'Abstract',
        blank=True,
    )

    doi = models.CharField(
        max_length=100,
        verbose_name=u'DOI',
        blank=True,
    )

    # pdf_link = models.

    # see_also = models.

    # language = models.

    # published = models.

    # tags and keywords

    # journal

    number = models.PositiveIntegerField(
        verbose_name=u'Number',
        blank=True,
        null=True,
    )

    volume = models.PositiveIntegerField(
        default=1,
        verbose_name=u'Volume',
        blank=True,
    )

    pages = models.CharField(
        max_length=25,
        verbose_name=u'Pages',
        blank=True,
    )

    issn = models.CharField(
        max_length=100,
        verbose_name=u'ISSN',
        blank=True,
    )

    isbn = models.CharField(
        max_length=100,
        verbose_name=u'ISBN',
        blank=True,
    )

    impact_factor = models.DecimalField(
        max_digits=10,
        decimal_places=8,
        verbose_name=u'Impact factor',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title))

        super(Publication, self).save(*args, **kwargs)
