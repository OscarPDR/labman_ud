# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *


###########################################################################
# Class: OrganizationSeeAlsoInline
###########################################################################

class OrganizationSeeAlsoInline(admin.TabularInline):
    model = OrganizationSeeAlso
    extra = 1


###########################################################################
# Class: OrganizationSeeAlsoAdmin
###########################################################################

class OrganizationSeeAlsoAdmin(admin.ModelAdmin):
    model = OrganizationSeeAlso

    list_display = ['organization', 'see_also']
    search_fields = ['organization__full_name']


###########################################################################
# Class: OrganizationAdmin
###########################################################################

class OrganizationAdmin(admin.ModelAdmin):
    model = Organization

    search_fields = ['full_name', 'short_name']
    list_display = ['full_name', 'short_name', 'organization_type']
    list_filter = ['country__full_name', 'organization_type']
    exclude = [
        'slug',
    ]
    inlines = [
        OrganizationSeeAlsoInline,
    ]


###########################################################################
# Class: UnitAdmin
###########################################################################

class UnitAdmin(admin.ModelAdmin):
    model = Unit

    list_display = ['organization', 'head', 'order']


###########################################################################
###########################################################################
# Register classes
###########################################################################
###########################################################################

admin.site.register(OrganizationSeeAlso, OrganizationSeeAlsoAdmin)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Unit, UnitAdmin)
