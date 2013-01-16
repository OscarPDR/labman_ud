# coding: utf-8

from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify

from organization_manager.models import Organization

# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=25, verbose_name='Nombre')
    first_surname = models.CharField(max_length=25, verbose_name='Primer Apellido')
    second_surname = models.CharField(max_length=25, verbose_name='Segundo Apellido')
    foaf_link = models.URLField(max_length=200, verbose_name='Perfil FOAF')
    slug = models.SlugField()

    def __unicode__(self):
        return u'%s %s %s' % (self.name, self.first_surname, self.second_surname)

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.name) + str(" ") + str(self.first_surname) + str(" ") + str(self.second_surname))
        super(Employee, self).save(*args, **kwargs)

class Job(models.Model):
    employee = models.ForeignKey(Employee)
    place = models.ForeignKey(Organization)
    start_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name='Mes de inicio')
    start_year = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(2020)], verbose_name='Año de inicio')
    end_month = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(12)], verbose_name='Mes de fin')
    start_year = models.IntegerField(validators=[MinValueValidator(1990), MaxValueValidator(2020)], verbose_name='Año de fin')
