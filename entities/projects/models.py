# coding: utf-8

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

from entities.persons.models import Person
from entities.funding_programs.models import FundingProgram
from entities.organizations.models import Organization
from entities.publications.models import Publication

from entities.utils.models import Role, Tag


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
    ('01', 'January'),
    ('02', 'February'),
    ('03', 'March'),
    ('04', 'April'),
    ('05', 'May'),
    ('06', 'June'),
    ('07', 'July'),
    ('08', 'August'),
    ('09', 'September'),
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
    )

    slug = models.SlugField(
        max_length=100,
        blank=True,
        unique=True,
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
        self.slug = slugify(self.name.encode('utf-8'))
        super(ProjectType, self).save(*args, **kwargs)


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
        max_length=250,
        blank=True,
    )

    slug = models.SlugField(
        max_length=250,
        blank=True,
        unique=True,
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
        default='01',
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

    observations = models.TextField(
        max_length=1000,
        blank=True,
    )

    funding_programs = models.ManyToManyField(FundingProgram, through='Funding', related_name='projects')
    persons = models.ManyToManyField(Person, through='AssignedPerson', related_name='projects')
    organizations = models.ManyToManyField(Organization, through='ConsortiumMember', related_name='projects')
    tags = models.ManyToManyField(Tag, through='ProjectTag', related_name='projects')
    publications = models.ManyToManyField(Publication, through='RelatedPublication', related_name='projects')

    class Meta:
        ordering = ['slug']

    def __unicode__(self):
        return u'%s' % (self.full_name)

    def save(self, *args, **kwargs):
        if not self.short_name:
            self.short_name = self.full_name.encode('utf-8')

        self.slug = slugify(str(self.short_name))
        super(Project, self).save(*args, **kwargs)


#########################
# Model: ProjectLogo
#########################

class ProjectLogo(models.Model):
    project = models.ForeignKey(Project, related_name='project_logos')

    logo = models.ImageField(
        upload_to=project_logo_path,
        blank=True,
        null=True,
    )

    def __unicode__(self):
        return u'Logo for project: %s' % (self.project.short_name)


#########################
# Model: Funding
#########################

class Funding(models.Model):
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
        return u'%s funded by %s - Project code: %s' % (self.project.short_name, self.funding_program.short_name, self.project_code)


#########################
# Model: FundingAmount
#########################

class FundingAmount(models.Model):
    funding = models.ForeignKey(Funding, related_name='funding_amounts')

    consortium_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    own_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        blank=True,
        null=True,
    )

    year = models.IntegerField(
        validators=[MinValueValidator(MIN_YEAR_LIMIT), MaxValueValidator(MAX_YEAR_LIMIT)],
        blank=True,
    )

    def __unicode__(self):
        return u'Year %s - (%s € Deusto / %s € Consortium)' % (self.year, self.own_amount, self.consortium_amount)


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


#########################
# Model: ProjectTag
#########################

class ProjectTag(models.Model):
    tag = models.ForeignKey(Tag)
    project = models.ForeignKey(Project)

    def __unicode__(self):
        return u'%s tagged as: %s' % (self.project.full_name, self.tag.tag)


#########################
# Model: RelatedPublication
#########################

class RelatedPublication(models.Model):
    project = models.ForeignKey(Project)

    publication = models.ForeignKey(Publication)

    def __unicode__(self):
        return u'Project: %s - Publication: %s' % (self.project.short_name, self.publication.title)
