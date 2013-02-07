# coding: utf-8

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

from organization_manager.models import Organization

GEOGRAPHICAL_SCOPE = (
    ('Araba', 'Araba'),
    ('Bizkaia', 'Bizkaia'),
    ('Gipuzkoa', 'Gipuzkoa'),
    ('Euskadi', 'Euskadi'),
    ('Spain', 'Spain'),
    ('Europe', 'Europe'),
    ('International', 'International'),
)

# Create your models here.


def funding_program_logo_path(self, filename):
    return "%s/%s%s" % ("funding_calls", self.slug, os.path.splitext(filename)[-1])


#########################
# Model: FundingCall
#########################

class FundingCall(models.Model):
    organization = models.ForeignKey(Organization)

    full_name = models.CharField(
        max_length = 100,
        verbose_name = 'Funding call full name',
    )

    short_name = models.CharField(
        max_length = 100,
        verbose_name = 'Funding call short name',
        blank = True,
    )

    concession_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name = 'Concession year',
        blank = True,
        null = True,
    )

    geographical_scope = models.CharField(
        max_length = 25,
        choices = GEOGRAPHICAL_SCOPE,
        default = 'Province',
        verbose_name = 'Geographical scope',
        blank = True,
    )

    logo = models.ImageField(
        upload_to = funding_program_logo_path,
        verbose_name = 'Logo',
        blank = True,
        null = True,
    )

    slug = models.SlugField(
        max_length = 100,
        blank = True,
    )

    def __unicode__(self):
        return u'%s, %s' % (self.full_name, self.organization.name)

    def save(self, *args, **kwargs):
        if self.slug == "":
            if self.short_name != "":
                self.slug = slugify(str(self.short_name))
            else:
                self.slug = slugify(str(self.full_name))
        super(FundingCall, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        if self.logo:
            storage = self.logo.storage
            path = self.logo.path
            # Delete the model before the file
            super(FundingCall, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)
        else:
            super(FundingCall, self).delete(*args, **kwargs)

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
