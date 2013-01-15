# coding: utf-8

import os

from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.template.defaultfilters import slugify
from django.core.files.storage import FileSystemStorage

# from organization_manager.models import Organization
# from employee_manager.models import Employee

PROJECT_TYPES = (
    ('Project', 'Proyecto'),
    ('DevelopmentProject', 'Proyecto de desarrollo'),
    ('InnovationProject', 'Proyecto de innovación'),
    ('ResearchProject', 'Proyecto de investigación'),
    ('BasicResearchProject', 'Proyecto de investigación básica'),
    ('AppliedResearchProject', 'Proyecto de investigación aplicada'),
)

PROJECT_STATUS = (
    ('NotStarted', 'Sin comenzar'),
    ('InDevelopment', 'En desarrollo'),
    ('Finished', 'Finalizado'),
)

CURRENCIES = (
    ('Euro', 'Euro'),
    ('Dollar', 'Dólar'),
)

GEOGRAPHICAL_SCOPE = (
    ('Province', 'Provincia'),
    ('State', 'Comunidad autónoma'),
    ('Country', 'País'),
)

# Create your models here.

def logo_path(self, filename):
    return self.slug + os.path.splitext(filename)[-1]


class Project(models.Model):
    project_type = models.CharField(
        max_length = 25,
        choices = PROJECT_TYPES,
        default = 'Project',
        verbose_name = 'Tipo de proyecto'
    )

    title = models.CharField(
        max_length = 100,
        verbose_name = 'Título'
    )

    description = models.TextField(
        max_length = 500,
        verbose_name = 'Descripción'
    )

    homepage = models.URLField(
        max_length = 150,
        verbose_name = 'Web'
    )

    start_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2015)],
        verbose_name = 'Año de comienzo'
    )

    end_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2015)],
        verbose_name = 'Año de fin'
    )

    status = models.CharField(
        max_length = 25,
        choices = PROJECT_STATUS,
        default = 'NotStarted',
        verbose_name = 'Estado'
    )

    # total_funds =

    currency = models.CharField(
        max_length = 25,
        choices = CURRENCIES,
        default = 'Euro',
        verbose_name = 'Moneda'
    )

    # additional_info
    # tag

    observations = models.TextField(
        max_length = 500,
        verbose_name = 'Observaciones'
    )

    logo = models.ImageField(
        upload_to = logo_path,
        verbose_name = 'Logotipo',
        blank = True,
        null = True,
    )

    slug = models.SlugField()

    def save(self, *args, **kwargs):
        self.slug = slugify(str(self.title))
        print "Proyecto guardado"
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
        path = self.logo.path

        os.remove(path)

        # Delete the file after the model
        storage.delete(path)

class FundingProgram(models.Model):
    project = models.ForeignKey(Project)

    name = models.CharField(
        max_length = 25,
        verbose_name = 'Nombre del programa',
    )

    project_code = models.CharField(
        max_length = 25,
        verbose_name = 'Código del proyecto',
    )

    start_month = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(12)],
        verbose_name = 'Mes de comienzo'
    )

    start_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2015)],
        verbose_name = 'Año de comienzo'
    )

    end_month = models.IntegerField(
        validators = [MinValueValidator(1), MaxValueValidator(12)],
        verbose_name = 'Mes de fin'
    )

    end_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2015)],
        verbose_name = 'Año de fin'
    )

    concession_year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2015)],
        verbose_name = 'Año de concesión'
    )

    geographical_scope = models.CharField(
        max_length = 25,
        choices = GEOGRAPHICAL_SCOPE,
        default = 'Province',
        verbose_name = 'Tipo de proyecto'
    )

    # logo = models.ImageField(
    #     upload_to = logo_path,
    #     verbose_name = 'Logotipo',
    #     blank = True,
    #     null = True,
    # )

    def delete(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage = self.logo.storage
        path = self.logo.path
        # Delete the model before the file
        super(FundingProgram, self).delete(*args, **kwargs)
        # Delete the file after the model
        storage.delete(path)

    def update(self, *args, **kwargs):
        # You have to prepare what you need before delete the model
        storage = self.logo.storage
        path = self.logo.path

        os.remove(path)

        # Delete the file after the model
        storage.delete(path)


class FundingAmount(models.Model):
    project = models.ForeignKey(Project)

    amount = models.DecimalField(
        max_digits = 5,
        decimal_places = 2,
    )

    year = models.IntegerField(
        validators = [MinValueValidator(1990), MaxValueValidator(2015)],
        verbose_name = 'Año de concesión'
    )
