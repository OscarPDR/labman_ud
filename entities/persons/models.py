# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify

from entities.organizations.models import Organization


# Create your models here.


def person_profile_picture_path(self, filename):
    return "%s/%s%s" % ("persons", self.slug, os.path.splitext(filename)[-1])


#########################
# Model: Person
#########################

class Person(models.Model):
    first_name = models.CharField(
        max_length=25,
    )

    first_surname = models.CharField(
        max_length=50,
    )

    second_surname = models.CharField(
        max_length=50,
        blank=True,
    )

    full_name = models.CharField(
        max_length=150,
        blank=True,
    )

    foaf_link = models.URLField(
        max_length=200,
        blank=True,
        null=True,
    )

    external = models.BooleanField(
        blank=True,
    )

    organization = models.ForeignKey(
        Organization,
        blank=True,
        null=True
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,
    )

    profile_picture = models.ImageField(
        upload_to=person_profile_picture_path,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        full_name = self.first_name + ' ' + self.first_surname

        if self.second_surname:
            full_name = full_name + ' ' + self.second_surname

        self.full_name = full_name

        self.slug = slugify(self.full_name)
        super(Person, self).save(*args, **kwargs)


#########################
# Model: Role
#########################

class Role(models.Model):
    name = models.CharField(
        max_length=50,
    )

    slug = models.SlugField(
        max_length=50,
        blank=True,
        unique=True,
    )

    description = models.TextField(
        max_length=1500,
    )

    def __unicode__(self):
        return u'Role: %s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Role, self).save(*args, **kwargs)
