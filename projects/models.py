# coding: utf-8

import os

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.template.defaultfilters import slugify

from employees.models import Employee
from funding_programs.models import FundingProgram
from organizations.models import Organization

PROJECT_TYPES = (
    ('Project', 'Project'),
    ('Development project', 'Development project'),
    ('Innovation project', 'Innovation project'),
    ('Research project', 'Research project'),
    ('Basic research project', 'Basic research project'),
    ('Applied research project', 'Applied research project'),
)

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

GEOGRAPHICAL_SCOPE = (
    ('Araba', 'Araba'),
    ('Bizkaia', 'Bizkaia'),
    ('Gipuzkoa', 'Gipuzkoa'),
    ('Euskadi', 'Euskadi'),
    ('Spain', 'Spain'),
    ('Europe', 'Europe'),
    ('International', 'International'),
)

ROLES = (
    ('Researcher', 'Researcher'),
    ('Principal researcher', 'Principal researcher'),
    ('Project manager', 'Project manager'),
)

# Create your models here.


def project_logo_path(self, filename):
    return "%s/%s%s" % ("projects", self.slug, os.path.splitext(filename)[-1])


#########################
# Model: Project
#########################

class Project(models.Model):
    funding_program = models.ForeignKey(FundingProgram, verbose_name = 'Funding program *')     # Required
    project_leader = models.ForeignKey(Organization, verbose_name = "Leader organization *")      # Required

    project_type = models.CharField(
        max_length = 50,
        choices = PROJECT_TYPES,
        default = 'Project',
        verbose_name = 'Project type *',     # Required
    )

    title = models.CharField(
        max_length = 150,
        verbose_name = 'Title *',    # Required
    )

    slug = models.SlugField(
        max_length = 150,
        blank = True,
    )

    description = models.TextField(
        max_length = 1000,
        verbose_name = 'Description *',     # Required
    )

    homepage = models.URLField(
        max_length = 150,
        verbose_name = 'Homepage',
        blank = True,
        null = True,
    )

    start_month = models.CharField(
        max_length= 25,
        choices = MONTHS,
        default = '1',
        verbose_name = 'Start month',
        blank = True,
    )

    start_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name = 'Start year *',      # Required
    )

    end_month = models.CharField(
        max_length= 25,
        choices = MONTHS,
        default = '12',
        verbose_name = 'End month',
        blank = True,
    )

    end_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2030)],
        verbose_name = 'End year *',    # Required
    )

    status = models.CharField(
        max_length = 25,
        choices = PROJECT_STATUS,
        default = 'NotStarted',
        verbose_name = 'Status *',      # Required
    )

    project_code = models.CharField(
        max_length = 100,
        verbose_name = 'Project code',
        blank = True,
    )

    total_funds = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = 'Total funds',
    )

    total_funds_deusto = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        blank = True,
        null = True,
        verbose_name = 'Total funds (Deusto)',
    )

    logo = models.ImageField(
        upload_to = project_logo_path,
        verbose_name = 'Logo',
        blank = True,
        null = True,
    )

    observations = models.TextField(
        max_length = 1000,
        verbose_name = 'Observations',
        blank = True,
    )

    def __unicode__(self):
        return u'%s' % (self.title)

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = slugify(str(self.title))
        super(Project, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        if self.logo:
            storage = self.logo.storage
            path = self.logo.path
            # Delete the model before the file
            super(Project, self).delete(*args, **kwargs)
            # Delete the file after the model
            storage.delete(path)
        else:
            super(Project, self).delete(*args, **kwargs)

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
# Model: AssignedEmployee
#########################

class AssignedEmployee(models.Model):
    project = models.ForeignKey(Project)
    employee = models.ForeignKey(Employee, verbose_name = "Employee *")     # Required

    role = models.CharField(
        max_length = 50,
        choices = ROLES,
        default = 'Researcher',
        verbose_name = 'Role *',    # Required
        blank = True,
    )

    def __unicode__(self):
        return u'%s - %s' % (self.employee, self.project)


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
