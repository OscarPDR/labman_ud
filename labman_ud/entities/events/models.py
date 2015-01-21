# -*- encoding: utf-8 -*-

import os

from django.db import models
from entities.core.models import BaseModel
from labman_ud.util import nslugify

from .linked_data import *

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
        null=True,
    )

    host_city = models.ForeignKey(
        'utils.City',
        blank=True,
        null=True,
    )

    host_country = models.ForeignKey(
        'utils.Country',
        blank=True,
        null=True,
    )

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
        verbose_name = u'Event'
        verbose_name_plural = u'Events'

    def __unicode__(self):
        return u'%s %s' % (self.short_name, self.year)

    def save(self, *args, **kwargs):
        old_slug = self.slug

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_event_rdf(self)

        if not self.short_name:
            self.short_name = self.full_name

        self.slug = nslugify(self.short_name, self.year)
        super(Event, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_event_as_rdf(self)
            update_event_object_triples(old_slug, self.slug)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_event_rdf(self)

        super(Event, self).delete(*args, **kwargs)


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

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_event_see_also_rdf(self)

        super(EventSeeAlso, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_event_see_also_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_event_see_also_rdf(self)

        super(EventSeeAlso, self).delete(*args, **kwargs)


###########################################################################
# Model: PersonRelatedToEvent
###########################################################################

class PersonRelatedToEvent(BaseModel):
    person = models.ForeignKey('persons.Person')
    event = models.ForeignKey('Event')

    class Meta:
        verbose_name = u'Person related to event'
        verbose_name_plural = u'People related to events'

    def __unicode__(self):
        return u'%s attended %s' % (self.person.full_name, self.event.full_name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_person_related_to_event_rdf(self)

        super(PersonRelatedToEvent, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_person_related_to_event_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_person_related_to_event_rdf(self)

        super(PersonRelatedToEvent, self).delete(*args, **kwargs)
