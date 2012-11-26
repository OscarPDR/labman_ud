# coding: utf-8

from django import forms
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

# from managers.organization_manager.models import Organization

# from managers.employee_manager.models import Employee

PROJECT_TYPES = (
    ('Project', 'Proyecto'),
    ('DevelopmentProject', 'Proyecto de desarrollo'),
    ('InnovationProject', 'Proyecto de innovación'),
    ('ResearchProject', 'Proyecto de investigación'),
    ('BasicResearchProject', 'Proyecto de investigación básica'),
    ('AppliedResearchProject', 'Proyecto de investigación aplicada'),
)

GEOGRAPHICAL_SCOPE = (
    ('Project', 'Proyecto'),
    ('DevelopmentProject', 'Proyecto'),
    ('InnovationProject', 'Proyecto'),
    ('ResearchProject', 'Proyecto'),
    ('BasicResearchProject', 'Proyecto'),
    ('AppliedResearchProject', 'Proyecto'),
)

# Create your models here.

class Project(models.Model):
	project_type = models.CharField(max_length = 25, choices = PROJECT_TYPES, default = 'Project', verbose_name = 'Tipo de proyecto')
	project_title = models.CharField(max_length = 100, verbose_name = 'Título')
	project_description = models.TextField(max_length = 500, verbose_name = 'Descripción')
	project_homepage = models.URLField(max_length = 150, verbose_name = 'Web')
	# additional_info
	# tag
	project_start_year = models.IntegerField(validators = [MinValueValidator(1990), MaxValueValidator(2015)], verbose_name = 'Año de comienzo')
	# project_end_year = 
	# project_status = 
	# project_logo = 
	# project_total_funds = 
	# # currency
	# project_observations =

# class FundingProgram(models.Model):
# 	funding_name =
# 	funding_project_code =  
# 	funding_start_month = 
# 	funding_start_year = 
# 	funding_end_month = 
# 	funding_end_year = 
# 	funding_concession_year = 
# 	funding_geographical_scope =
# 	funding_logo = 

# class FundingAmount(models.Model):
# 	funding_amount = 
# 	funding_year = 
# 	# currency
