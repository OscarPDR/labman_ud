# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify


def event_logo_path(self, filename):
    return '%s/%s%s' % ('events', self.slug, os.path.splitext(filename)[-1])


# Create your models here.

#########################
# Model: Event
#########################

class Event(models.Model):
    # type

    full_name = models.CharField(
        max_length=250,
        verbose_name=u'Full name *',    # Required
    )

    short_name = models.CharField(
        max_length=150,
        verbose_name=u'Short name',
        blank=True,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
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
        event_name = u'%s %s' % (self.short_name, self.year)
        self.slug = slugify(event_name)

        if (not self.year) and (self.start_date):
            self.year = self.start_date.year

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
