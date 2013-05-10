# coding: utf-8

from django.contrib import admin
from .models import Person, Role


#########################
# Class: PersonAdmin
#########################

class PersonAdmin(admin.ModelAdmin):
    model = Person
    list_filter = ['external']
    exclude = [
        'full_name',
        'slug',
    ]


#########################
# Class: RoleAdmin
#########################

class RoleAdmin(admin.ModelAdmin):
    model = Role
    exclude = [
        'slug',
    ]


##################################################
# Register classes
##################################################

admin.site.register(Person, PersonAdmin)
admin.site.register(Role, RoleAdmin)
