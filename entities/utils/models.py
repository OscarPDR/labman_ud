# coding: utf-8

from django.db import models
from django.template.defaultfilters import slugify


# Create your models here.


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

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super(Role, self).save(*args, **kwargs)


#########################
# Model: Tag
#########################

class Tag(models.Model):
    tag = models.CharField(
        max_length=50,
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
    )

    def __unicode__(self):
        return u'%s' % (self.tag)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.tag.encode('utf-8')))
        super(Role, self).save(*args, **kwargs)
