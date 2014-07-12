# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *


###########################################################################
# Class: FundingProgramSeeAlsoInline
###########################################################################

class FundingProgramSeeAlsoInline(admin.TabularInline):
    model = FundingProgramSeeAlso
    extra = 1


###########################################################################
# Class: FundingProgramSeeAlsoAdmin
###########################################################################

class FundingProgramSeeAlsoAdmin(admin.ModelAdmin):
    model = FundingProgramSeeAlso

    list_display = ['funding_program', 'see_also']
    search_fields = ['funding_program__full_name']


###########################################################################
# Class: FundingProgramLogoInline
###########################################################################

class FundingProgramLogoInline(admin.StackedInline):
    model = FundingProgramLogo
    extra = 1
    exclude = ['slug']


###########################################################################
# Class: FundingProgramAdmin
###########################################################################

class FundingProgramAdmin(admin.ModelAdmin):
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

admin.site.register(FundingProgramSeeAlso, FundingProgramSeeAlsoAdmin)
admin.site.register(FundingProgram, FundingProgramAdmin)
