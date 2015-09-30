# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *


###     OrganizationSeeAlsoInline
####################################################################################################

class OrganizationSeeAlsoInline(admin.TabularInline):
    model = OrganizationSeeAlso

    extra = 0


###     OrganizationAdmin
####################################################################################################

class OrganizationAdmin(admin.ModelAdmin):
    model = Organization

    search_fields = ['full_name', 'short_name']

    list_display = ['full_name', 'organization_type']

    list_filter = ['country__full_name', 'organization_type']

    exclude = ['slug']

    inlines = [
        OrganizationSeeAlsoInline,
    ]


###     UnitAdmin
####################################################################################################

class UnitAdmin(admin.ModelAdmin):
    model = Unit

    list_display = ['organization', 'head', 'order']


####################################################################################################
####################################################################################################
###     Register classes
####################################################################################################
####################################################################################################

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Unit, UnitAdmin)
