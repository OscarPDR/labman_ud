# coding: utf-8

import os

from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


def organization_logo_path(self, filename):
    return '%s/%s%s' % ('organizations', self.slug, os.path.splitext(filename)[-1])


#########################
# Model: Organization
#########################

class Organization(models.Model):
    name = models.CharField(
        max_length = 75,
        verbose_name = 'Name *',    # Required
    )

    country = models.CharField(
        max_length = 500,
        verbose_name = 'Country',
        blank = True,
    )

    homepage = models.URLField(
        verbose_name = 'Homepage',
        blank = True,
        null = True,
    )

    logo = models.ImageField(
        upload_to = organization_logo_path,
        verbose_name = 'Logo',
        blank = True,
        null = True,
    )

    slug = models.SlugField(
        max_length = 100,
        blank = True,
    )

    def __unicode__(self):
        return u'%s' % (self.name)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name))
        super(Organization, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        if self.logo:
            storage = self.logo.storage
            path = self.logo.path
            # Delete the model before the file
            super(Organization, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)
        else:
            super(Organization, self).delete(*args, **kwargs)

    def update(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage = self.logo.storage

        try:
            path = self.logo.path
            os.remove(path)
            # Delete the file after the model
            storage.delete(path)
        except:
            pass
            # No previous logo

    class Meta:
        ordering = ['name']
