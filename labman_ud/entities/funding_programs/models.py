# -*- encoding: utf-8 -*-

from django.db import models
from django.template.defaultfilters import slugify

from .linked_data import *

import os


def funding_program_logo_path(self, filename):
    return "%s/%s_%s%s" % ("funding_programs", self.funding_program.slug, self.slug, os.path.splitext(filename)[-1])


###		FundingProgram
####################################################################################################

class FundingProgram(models.Model):

    organization = models.ForeignKey('organizations.Organization')

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

    geographical_scope = models.ForeignKey('utils.GeographicalScope')

    observations = models.TextField(
        max_length=1000,
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['slug']
        verbose_name = u'Funding program'
        verbose_name_plural = u'Funding programs'

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.slug = slugify(self.short_name)

        super(FundingProgram, self).save(*args, **kwargs)


###		FundingProgramSeeAlso
####################################################################################################

class FundingProgramSeeAlso(models.Model):

    funding_program = models.ForeignKey('FundingProgram')

    see_also = models.URLField(
        max_length=512,
    )


###		FundingProgramLogo
####################################################################################################

class FundingProgramLogo(models.Model):

    funding_program = models.ForeignKey('FundingProgram')

    name = models.CharField(
        max_length=250,
        blank=True,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
    )

    logo = models.ImageField(
        max_length=250,
        upload_to=funding_program_logo_path,
        blank=True,
        null=True,
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(FundingProgramLogo, self).save(*args, **kwargs)
