# coding: utf-8

from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

class Organization(models.Model):
	organization_name = models.CharField(max_length = 25, verbose_name = 'Nombre')
	organization_country = models.TextField(max_length = 500, verbose_name = 'Descripción')
	organization_homepage = models.URLField(verbose_name = 'Número Pokédex')
	organization_logo = models.DecimalField(max_digits = 5, decimal_places = 2, verbose_name = 'Peso')