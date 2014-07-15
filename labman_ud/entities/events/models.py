# -*- encoding: utf-8 -*-

import os

from django.db import models
from django.template.defaultfilters import slugify
from entities.core.models import BaseModel


EVENT_TYPES = (
    ('Academic event', 'Academic event'),
    ('Generic event', 'Generic event'),
    ('Hackathon', 'Hackathon'),
    ('Project meeting', 'Project meeting'),
)


# Create your models here.


def event_logo_path(self, filename):
    return '%s/%s%s' % ('events', self.slug, os.path.splitext(filename)[-1])


###########################################################################
# Model: Event
###########################################################################

class Event(BaseModel):
    event_type = models.CharField(
        max_length=75,
        choices=EVENT_TYPES,
        default='Generic event',
    )

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

    host_city = models.ForeignKey('utils.City', blank=True, null=True)

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

    proceedings = models.ForeignKey('publications.Proceedings', blank=True, null=True, related_name='conference')

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
# Model: EventSeeAlso
###########################################################################

class EventSeeAlso(BaseModel):
    event = models.ForeignKey('Event')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.event.full_name, self.see_also)


###########################################################################
# Model: PersonRelatedToEvent
###########################################################################

class PersonRelatedToEvent(BaseModel):
    person = models.ForeignKey('persons.Person')
    event = models.ForeignKey('Event')

    def __unicode__(self):
        return u'%s attended %s' % (self.person.full_name, self.event.full_name)
