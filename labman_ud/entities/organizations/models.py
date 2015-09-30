# -*- encoding: utf-8 -*-

import os

from django.db import models
from django.template.defaultfilters import slugify

from .linked_data import *


ORGANIZATION_TYPES = (
    ('Association', 'Association'),
    ('Educational organization', 'Educational organization'),
    ('Enterprise', 'Enterprise'),
    ('Foundation', 'Foundation'),
    ('Public administration', 'Public administration'),
    ('Research group', 'Research group'),
    ('University', 'University'),
)


def organization_logo_path(self, filename):
    return '%s/%s%s' % ('organizations', self.slug, os.path.splitext(filename)[-1])


###		Organization()
####################################################################################################

class Organization(models.Model):

    organization_type = models.CharField(
        max_length=75,
        choices=ORGANIZATION_TYPES,
        default='Enterprise',
    )

    sub_organization_of = models.ForeignKey(
        'self',
        blank=True,
        null=True,
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

    country = models.ForeignKey(
        'utils.Country',
        blank=True,
        null=True,
    )

    homepage = models.URLField(
        blank=True,
        null=True,
    )

    logo = models.ImageField(
        upload_to=organization_logo_path,
        blank=True,
        null=True,
    )

    consortium_member_in = models.ManyToManyField(
        'projects.Project',
        through='projects.ConsortiumMember',
        related_name='organizations',
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        if self.short_name == self.full_name:
            return u'%s' % (self.full_name)
        else:
            return u'%s (%s)' % (self.short_name, self.full_name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_organization_rdf(self)

        if not self.short_name:
            self.short_name = self.full_name

        else:
            self.short_name = self.short_name

        self.slug = slugify(self.short_name.encode('utf-8'))

        super(Organization, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_organization_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_organization_rdf(self)

        super(Organization, self).delete(*args, **kwargs)


###		OrganizationSeeAlso()
####################################################################################################

class OrganizationSeeAlso(models.Model):

    organization = models.ForeignKey('Organization', related_name='see_also_links')

    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.organization.full_name, self.see_also)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_organization_see_also_rdf(self)

        super(OrganizationSeeAlso, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_organization_see_also_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_organization_see_also_rdf(self)

        super(OrganizationSeeAlso, self).delete(*args, **kwargs)


###		Unit()
####################################################################################################

class Unit(models.Model):

    organization = models.ForeignKey('Organization', related_name='unit')

    head = models.ForeignKey('persons.Person', null=True, blank=True)

    order = models.PositiveSmallIntegerField(
        unique=True,
    )

    class Meta:
        ordering = ['order']

    def __unicode__(self):
        return u'%s' % (self.organization.full_name)

    def save(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_unit_rdf(self)

        super(Unit, self).save(*args, **kwargs)

        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            save_unit_as_rdf(self)

    def delete(self, *args, **kwargs):
        # Publish RDF data
        if getattr(settings, 'ENABLE_RDF_PUBLISHING', False):
            delete_unit_rdf(self)

        super(Unit, self).delete(*args, **kwargs)
