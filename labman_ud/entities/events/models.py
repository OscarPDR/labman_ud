# -*- encoding: utf-8 -*-

import os

from django.db import models
from django.template.defaultfilters import slugify
from entities.core.models import BaseModel


# Create your models here.


def event_logo_path(self, filename):
    return '%s/%s%s' % ('events', self.slug, os.path.splitext(filename)[-1])


def viva_photo_path(self, filename):
    return "%s/%s%s" % ("vivas", self.slug, os.path.splitext(filename)[-1])


VIVA_RESULTS = (
    ('Apt', 'Apt'),
    ('Cum Laude', 'Cum Laude'),
    ('Cum Laude by unanimity', 'Cum Laude by unanimity'),
)


###########################################################################
# Model: EventType
###########################################################################

class EventType(BaseModel):
    name = models.CharField(
        max_length=100,
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(EventType, self).save(*args, **kwargs)


###########################################################################
# Model: Event
###########################################################################

class Event(BaseModel):
    event_type = models.ForeignKey('EventType')

    full_name = models.CharField(
        max_length=250,
    )

    short_name = models.CharField(
        max_length=250,
        blank=True,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    location = models.CharField(
        max_length=250,
        blank=True,
    )

    host_city = models.CharField(
        max_length=150,
        blank=True,
    )

    host_country = models.ForeignKey('utils.Country', blank=True, null=True)

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )

    year = models.PositiveIntegerField()

    homepage = models.URLField(
        verbose_name='Homepage',
        blank=True,
        null=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    observations = models.TextField(
        max_length=1500,
        blank=True,
    )

    logo = models.ImageField(
        upload_to=event_logo_path,
        verbose_name='Logo',
        blank=True,
        null=True,
    )

    proceedings = models.ForeignKey('publications.Publication', blank=True, null=True, related_name='conference')

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s %s' % (self.short_name, self.year)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name

        self.slug = slugify(self.short_name)
        super(Event, self).save(*args, **kwargs)


###########################################################################
# Model: Viva
###########################################################################

class Viva(BaseModel):
    date = models.DateField()

    result = models.CharField(
        max_length=250,
        choices=VIVA_RESULTS,
        default='Apt',
        blank=True,
    )

    held_at_university = models.ForeignKey('organizations.Organization')

    panel = models.ForeignKey('VivaPanel')


###########################################################################
# Model: VivaPanel
###########################################################################

class VivaPanel(BaseModel):
    chair = models.ForeignKey(
        'persons.Person',
        related_name='is_chair',
    )

    chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_chairs_organization',
    )

    first_co_chair = models.ForeignKey(
        'persons.Person',
        related_name='is_first_co_chair',
    )

    first_co_chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_first_co_chairs_organization',
    )

    second_co_chair = models.ForeignKey(
        'persons.Person',
        related_name='is_second_co_chair',
    )

    second_co_chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_second_co_chairs_organization',
    )

    third_co_chair = models.ForeignKey(
        'persons.Person',
        related_name='is_third_co_chair',
    )

    third_co_chairs_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_third_co_chairs_organization',
    )

    secretary = models.ForeignKey(
        'persons.Person',
        related_name='is_secretary',
    )

    secretarys_organization = models.ForeignKey(
        'organizations.Organization',
        related_name='is_secretarys_organization',
    )
