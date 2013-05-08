# coding: utf-8

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

from persons.models import Person
from funding_programs.models import FundingProgram
from organizations.models import Organization

from utils.models import Role


# Create your models here.


def project_logo_path(self, filename):
    return "%s/%s%s" % ("projects", self.slug, os.path.splitext(filename)[-1])


MIN_YEAR_LIMIT = 2000
MAX_YEAR_LIMIT = 2020


PROJECT_STATUS = (
    ('Not started', 'Not started'),
    ('In development', 'In development'),
    ('Finished', 'Finished'),
)

MONTHS = (
    ('1', 'January'),
    ('2', 'February'),
    ('3', 'March'),
    ('4', 'April'),
    ('5', 'May'),
    ('6', 'June'),
    ('7', 'July'),
    ('8', 'August'),
    ('9', 'September'),
    ('10', 'October'),
    ('11', 'November'),
    ('12', 'December'),
)


#########################
# Model: ProjectType
#########################

class ProjectType(models.Model):
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
        super(ProjectType, self).save(*args, **kwargs)


ROLES = (
    ('Researcher', 'Researcher'),
    ('Principal researcher', 'Principal researcher'),
    ('Project manager', 'Project manager'),
)


#########################
# Model: Project
#########################

class Project(models.Model):
    project_leader = models.ForeignKey(Organization)

    project_type = models.ForeignKey(ProjectType)

    full_name = models.CharField(
        max_length=250,
    )

    short_name = models.CharField(
        max_length=150,
    )

    slug = models.SlugField(
        max_length=150,
        blank=True,
    )

    description = models.TextField(
        max_length=3000,
    )

    homepage = models.URLField(
        max_length=150,
        blank=True,
        null=True,
    )

    start_month = models.CharField(
        max_length=25,
        choices=MONTHS,
        default='1',
        blank=True,
    )

    start_year = models.IntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    end_month = models.CharField(
        max_length=25,
        choices=MONTHS,
        default='12',
        blank=True,
    )

    end_year = models.IntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
    )

    status = models.CharField(
        max_length=25,
        choices=PROJECT_STATUS,
        default='Not started',
    )

    # project_code = models.CharField(
    #     max_length=100,
    #     verbose_name='Project code',
    #     blank=True,
    # )



    # total_funds_deusto = models.DecimalField(
    #     max_digits=10,
    #     decimal_places=2,
    #     blank=True,
    #     null=True,
    #     verbose_name='Total funds (Deusto)',
    # )

    # logo = models.ImageField(
    #     upload_to=project_logo_path,
    #     verbose_name='Logo',
    #     blank=True,
    #     null=True,
    # )

    observations = models.TextField(
        max_length=1000,
        verbose_name='Observations',
        blank=True,
    )

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(str(self.title))
        super(Project, self).save(*args, **kwargs)


#########################
# Model: ProjectLogo
#########################

class ProjectLogo(models.Model):
    project = models.ForeignKey(Project)

    logo = models.ImageField(
        upload_to=project_logo_path,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'Logo for project: %s' % (self.project.short_name)


#########################
# Model: FundedProject
#########################

class FundedProject(models.Model):
    project = models.ForeignKey(Project)

    funding_program = models.ForeignKey(FundingProgram)

    project_code = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )

    total_funds = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'%s funded with %s by %s - Project code: %s' % (self.project.full_name, self.total_funds, self.funding_program.short_name, self.project_code)


#########################
# Model: FundingAmount
#########################

class FundingAmount(models.Model):
    funded_project = models.ForeignKey(FundedProject)

    consortium_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
    )

    own_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
    )

    year = models.IntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
        blank=True,
    )

    def __unicode__(self):
        return u'Year %s - %s €' % (self.year, self.amount)


#########################
# Model: AssignedPerson
#########################

class AssignedPerson(models.Model):
    project = models.ForeignKey(Project)

    person = models.ForeignKey(Person)

    role = models.ForeignKey(Role)

    def __unicode__(self):
        return u'%s is working at %s as a %s' % (self.person.full_name, self.project.short_name, self.role.name)


#########################
# Model: ConsortiumMember
#########################

class ConsortiumMember(models.Model):
    project = models.ForeignKey(Project)

    organization = models.ForeignKey(Organization)

    def __unicode__(self):
        return u'%s is taking part in %s' % (self.organization.short_name, self.project.short_name)
