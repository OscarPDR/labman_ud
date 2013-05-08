# coding: utf-8

from django.contrib import admin
from .models import Country, GeographicalScope


#########################
# Class: CountryAdmin
#########################

class CountryAdmin(admin.ModelAdmin):
    model = Country


#########################
# Class: GeographicalScopeAdmin
#########################

class GeographicalScopeAdmin(admin.ModelAdmin):
    model = GeographicalScope


##################################################
# Register classes
##################################################

admin.site.register(Country, CountryAdmin)
admin.site.register(GeographicalScope, GeographicalScopeAdmin)
