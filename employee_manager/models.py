# coding: utf-8

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

from organization_manager.models import Organization

# Create your models here.


#########################
# Model: Employee
#########################

class Employee(models.Model):
    name = models.CharField(
        max_length = 25,
        verbose_name = 'Name',
    )

    first_surname = models.CharField(
        max_length = 25,
        verbose_name = 'First surname',
    )

    second_surname = models.CharField(
        max_length = 25,
        verbose_name = 'Second surname',
        blank = True,
    )

    foaf_link = models.URLField(
        max_length = 200,
        verbose_name = 'FOAF profile',
        blank = True,
        null = True,
    )

    slug = models.SlugField()

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.first_surname, self.second_surname)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + str(' ' + self.first_surname) + str(' ' + self.second_surname))
        super(Employee, self).save(*args, **kwargs)


#########################
# Model: Job
#########################

class Job(models.Model):
    employee = models.ForeignKey(Employee)
    place = models.ForeignKey(Organization)

    start_month = models.IntegerField(
        validators = [
            MinValueValidator(1),
            MaxValueValidator(12)
        ],
        verbose_name = 'Start month'
    )

    start_year = models.IntegerField(
        validators = [
            MinValueValidator(1990),
            MaxValueValidator(2030)
        ],
        verbose_name = 'Start year'
    )

    end_month = models.IntegerField(
        validators = [
            MinValueValidator(1),
            MaxValueValidator(12)
        ],
        verbose_name = 'End month'
    )

    start_year = models.IntegerField(
        validators = [
            MinValueValidator(1990),
            MaxValueValidator(2030)
        ],
        verbose_name = 'End year'
    )
