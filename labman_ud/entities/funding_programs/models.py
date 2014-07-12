# -*- encoding: utf-8 -*-

import os

from django.db import models
from django.template.defaultfilters import slugify
from entities.core.models import BaseModel


# Create your models here.


def funding_program_logo_path(self, filename):
    return "%s/%s_%s%s" % ("funding_programs", self.funding_program.slug, self.slug, os.path.splitext(filename)[-1])


###########################################################################
# Model: FundingProgram
###########################################################################

class FundingProgram(BaseModel):
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

    def __unicode__(self):
        return u'%s, %s' % (self.full_name, self.organization.full_name)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.slug = slugify(self.short_name)

        super(FundingProgram, self).save(*args, **kwargs)


###########################################################################
# Model: FundingProgramSeeAlso
###########################################################################

class FundingProgramSeeAlso(BaseModel):
    funding_program = models.ForeignKey('FundingProgram')
    see_also = models.URLField(
        max_length=512,
    )

    def __unicode__(self):
        return u'%s related resource: %s' % (self.funding_program.full_name, self.see_also)


###########################################################################
# Model: FundingProgramLogo
###########################################################################

class FundingProgramLogo(BaseModel):
    funding_program = models.ForeignKey('FundingProgram')

    name = models.CharField(
        max_length=100,
        blank=True,
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,
    )

    logo = models.ImageField(
        upload_to=funding_program_logo_path,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'Logo for funding program: %s' % (self.funding_program.short_name)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        super(FundingProgramLogo, self).save(*args, **kwargs)
