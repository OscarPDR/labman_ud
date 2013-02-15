# coding: utf-8

from django.db import models
from django.template.defaultfilters import slugify

from organizations.models import Organization

# Create your models here.


#########################
# Model: Employee
#########################

class Employee(models.Model):
    name = models.CharField(
        max_length = 25,
        verbose_name = 'Name *',    # Required
    )

    first_surname = models.CharField(
        max_length = 25,
        verbose_name = 'First surname *',     # Required
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

    external = models.BooleanField(
        blank = True,
    )

    organization = models.ForeignKey(Organization, blank = True, null = True)

    slug = models.SlugField(
        max_length = 100,
        blank = True,
    )

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.first_surname, self.second_surname)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + str(' ' + self.first_surname) + str(' ' + self.second_surname))
        super(Employee, self).save(*args, **kwargs)

    class Meta:
        ordering = ['name', 'first_surname', 'second_surname']
