# coding: utf-8

from django.contrib import admin
from .models import Country, GeographicalScope, Role


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


#########################
# Class: RoleAdmin
#########################

class RoleAdmin(admin.ModelAdmin):
    model = Role


##################################################
# Register classes
##################################################

admin.site.register(Country, CountryAdmin)
admin.site.register(GeographicalScope, GeographicalScopeAdmin)
admin.site.register(Role, RoleAdmin)
