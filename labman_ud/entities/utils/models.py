# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.


def network_icon_path(self, filename):
    return "%s/%s%s" % ("networks", self.slug, os.path.splitext(filename)[-1])


#########################
# Model: Country
#########################

class Country(models.Model):
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
    )

    identifier_code = models.CharField(
        max_length=10,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')
        self.slug = slugify(self.short_name)
        super(Country, self).save(*args, **kwargs)


#########################
# Model: GeographicalScope
#########################

class GeographicalScope(models.Model):
    name = models.CharField(
        max_length=100,
        verbose_name=u'Name',
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
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
        self.slug = slugify(str(self.name))
        super(GeographicalScope, self).save(*args, **kwargs)


#########################
# Model: Role
#########################

class Role(models.Model):
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

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super(Role, self).save(*args, **kwargs)


#########################
# Model: Tag
#########################

class Tag(models.Model):
    name = models.CharField(
        max_length=75,
    )

    slug = models.SlugField(
        max_length=75,
        blank=True,
        unique=True,
    )

    sub_tag_of = models.ForeignKey(
        'self',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        name = self.name
        if self.sub_tag_of:
            name = name + ' < ' + self.sub_tag_of.name

        return u'%s' % (name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(Tag, self).save(*args, **kwargs)


#########################
# Model: Language
#########################

class Language(models.Model):
    name = models.CharField(
        max_length=50,
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
    )

    identifier_code = models.CharField(
        max_length=10,
        blank=True,
    )

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(Language, self).save(*args, **kwargs)


#########################
# Model: Network
#########################

class Network(models.Model):
    name = models.CharField(
        max_length=150,
    )

    base_url = models.URLField(
        max_length=250,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
    )

    # Recommended size: 64*64 px
    # Recommended format: .png
    icon = models.ImageField(
        upload_to=network_icon_path,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name.encode('utf-8')))
        super(Network, self).save(*args, **kwargs)


#########################
# Model: PhDProgram
#########################

class PhDProgram(models.Model):
    name = models.CharField(
        max_length=500,
    )

    university = models.ForeignKey(
        'organizations.Organization',
        related_name='university_holding_a_phd_program',
    )

    faculty = models.ForeignKey(
        'organizations.Organization',
        related_name='faculty_holding_a_phd_program',
        blank=True,
    )

    homepage = models.URLField(
        max_length=250,
    )

    start_date = models.DateField(
        blank=True,
        null=True,
    )

    end_date = models.DateField(
        blank=True,
        null=True,
    )
