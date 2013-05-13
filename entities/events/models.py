# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.


def event_logo_path(self, filename):
    return '%s/%s%s' % ('events', self.event.slug, os.path.splitext(filename)[-1])


#########################
# Model: EventType
#########################

class EventType(models.Model):
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

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(EventType, self).save(*args, **kwargs)


#########################
# Model: Event
#########################

class Event(models.Model):
    event_type = models.ForeignKey(EventType)

    full_name = models.CharField(
        max_length=250,
    )

    short_name = models.CharField(
        max_length=150,
        blank=True,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
        unique=True,
    )

    description = models.TextField(
        max_length=1500,
        blank=True,
    )

    location = models.CharField(
        max_length=150,
        verbose_name=u'Location',
        blank=True,
    )

    start_date = models.DateField(
        blank=True,
    )

    end_date = models.DateField(
        blank=True,
    )

    year = models.PositiveIntegerField(
        blank=True,
    )

    homepage = models.URLField(
        verbose_name='Homepage',
        blank=True,
        null=True,
    )

    observations = models.TextField(
        max_length=1500,
        blank=True,
    )

    def __unicode__(self):
        return u'%s %s' % (self.short_name, self.year)

    def save(self, *args, **kwargs):
        if (not self.year) and (self.start_date):
            self.year = self.start_date.year

        event_name = u'%s %s' % (self.short_name, self.year)
        self.slug = slugify(event_name)

        super(Event, self).save(*args, **kwargs)


#########################
# Model: EventLogo
#########################

class EventLogo(models.Model):
    event = models.ForeignKey(Event)

    logo = models.ImageField(
        upload_to=event_logo_path,
        verbose_name='Logo',
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'Logo for event: %s' % (self.event.short_name)
