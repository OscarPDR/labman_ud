# coding: utf-8

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

from persons.models import Person
from funding_programs.models import FundingProgram
from organizations.models import Organization


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
    funding_program = models.ForeignKey(FundingProgram, verbose_name='Funding program *')     # Required
    project_leader = models.ForeignKey(Organization, verbose_name="Leader organization *")      # Required

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

    total_funds = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

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
# Model: FundingAmount
#########################

class FundingAmount(models.Model):
    project = models.ForeignKey(Project)

    amount = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        verbose_name = 'Amount',
        blank = True,
    )

    year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name = 'Concession year',
        blank = True,
    )

    def __unicode__(self):
        return u'Year %s - %s €' % (self.year, self.amount)


#########################
# Model: AssignedPerson
#########################

class AssignedPerson(models.Model):
    project = models.ForeignKey(Project)
    person = models.ForeignKey(Person, verbose_name = "Person *")     # Required

    role = models.CharField(
        max_length = 50,
        choices = ROLES,
        default = 'Researcher',
        verbose_name = 'Role *',    # Required
        blank = True,
    )

    def __unicode__(self):
        return u'%s - %s' % (self.person, self.project)


#########################
# Model: ConsortiumMember
#########################

class ConsortiumMember(models.Model):
    project = models.ForeignKey(Project)
    organization = models.ForeignKey(Organization, verbose_name = "Organization *")     # Required

    class Meta:
        ordering = ["organization"]

    def __unicode__(self):
        return u'Project: %s - Organization: %s' % (self.project.title, self.organization.name)
