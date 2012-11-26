# coding: utf-8

from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# from managers.organization_manager.models import Organization

# Create your models here.

class Employee(models.Model):
	employee_name = models.CharField(max_length = 25, verbose_name = 'Nombre')
	first_surname = models.CharField(max_length = 25, verbose_name = 'Primer Apellido')
	second_surname = models.CharField(max_length = 25, verbose_name = 'Segundo Apellido')
	foaf_link = models.URLField(max_length = 200, verbose_name = 'Perfil FOAF')

class Job(models.Model):
	employee = models.ForeignKey(Employee)
	# start_date = models.CharField(max_length = 25, verbose_name = 'Ataque')
	# end_date = models.IntegerField(validators = [MinValueValidator(1), MaxValueValidator(100)], verbose_name = 'Nivel')
	# place = models.ForeignKey(Organization)
