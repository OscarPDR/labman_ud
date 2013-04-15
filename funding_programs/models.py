# coding: utf-8

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

from organizations.models import Organization

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
    return "%s/%s%s" % ("funding_programs", self.slug, os.path.splitext(filename)[-1])


#########################
# Model: FundingProgram
#########################

class FundingProgram(models.Model):
    organization = models.ForeignKey(Organization, verbose_name = 'Organization *')

    full_name = models.CharField(
        max_length = 250,
        verbose_name = 'Funding call full name',
    )

    short_name = models.CharField(
        max_length = 150,
        verbose_name = 'Funding call short name',
        blank = True,
    )

    concession_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name = 'Concession year *',
    )

    geographical_scope = models.CharField(
        max_length = 50,
        choices = GEOGRAPHICAL_SCOPE,
        default = 'Spain',
        verbose_name = 'Geographical scope *',
    )

    logo = models.ImageField(
        upload_to = funding_program_logo_path,
        verbose_name = 'Logo',
        blank = True,
        null = True,
    )

    observations = models.TextField(
        max_length = 1000,
        verbose_name = 'Observations',
        blank = True,
        null = True,
    )

    slug = models.SlugField(
        max_length = 150,
        blank = True,
    )

    def __unicode__(self):
        return u'%s, %s' % (self.full_name, self.organization.name)

    def save(self, *args, **kwargs):
        if self.short_name == "":
            self.short_name = self.full_name
        self.short_name = self.short_name.encode('utf-8')
        self.slug = slugify(self.short_name)
        super(FundingProgram, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        if self.logo:
            storage = self.logo.storage
            path = self.logo.path
            # Delete the model before the file
            super(FundingProgram, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)
        else:
            super(FundingProgram, self).delete(*args, **kwargs)

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
