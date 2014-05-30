# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import FundingProgram, FundingProgramLogo


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
        FundingProgramLogoInline,
    ]


##################################################
# Register classes
##################################################

admin.site.register(FundingProgram, FundingProgramAdmin)
