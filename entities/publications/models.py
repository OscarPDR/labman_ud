# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify

from entities.events.models import Event


# Create your models here.


def publication_path(self, filename):
    if self.presented_at:
        year = self.presented_at.year
        sub_folder = self.presented_at.slug
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
    presented_at = models.ForeignKey(
        Event,
        blank=True,
        null=True,
    )

    publication_type = models.ForeignKey(PublicationType)

    title = models.CharField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
    )

    abstract = models.TextField(
        max_length=5000,
        blank=True,
    )

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

    # see_also = models.

    # language = models.

    # published = models.

    # tags and keywords

    # journal

    number = models.PositiveIntegerField(
        blank=True,
        null=True,
    )

    volume = models.PositiveIntegerField(
        default=1,
        blank=True,
    )

    pages = models.CharField(
        max_length=25,
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
