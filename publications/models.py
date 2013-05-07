# coding: utf-8

from django.db import models

from events.models import Event


# Create your models here.

#########################
# Model: Publication
#########################

class Publication(models.Model):
    presented_at = models.ForeignKey(Event)

    # type

    title = models.CharField(
        max_length=150,
        verbose_name=u'Title *',    # Required
    )

    abstract = models.TextField(
        max_length=1500,
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

    number = models.PositiveIntegerField(
        default=1,
        verbose_name=u'Number',
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
    )
