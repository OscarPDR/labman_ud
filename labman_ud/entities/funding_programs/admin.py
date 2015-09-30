# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *


###     FundingProgramSeeAlsoInline
####################################################################################################

class FundingProgramSeeAlsoInline(admin.TabularInline):
    model = FundingProgramSeeAlso

    extra = 0


###     FundingProgramLogoInline
####################################################################################################

class FundingProgramLogoInline(admin.TabularInline):
    model = FundingProgramLogo

    extra = 0
    exclude = ['slug']


###     FundingProgramAdmin
####################################################################################################

class FundingProgramAdmin(admin.ModelAdmin):
    model = FundingProgram

    search_fields = ['full_name', 'short_name']

    list_display = ['short_name', 'full_name', 'geographical_scope']

    list_filter = ['geographical_scope']

    exclude = ['slug']

    inlines = [
        FundingProgramSeeAlsoInline,
        FundingProgramLogoInline,
    ]


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(FundingProgram, FundingProgramAdmin)
