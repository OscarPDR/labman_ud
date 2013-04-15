# coding: utf-8

from django.contrib import admin
from funding_programs.models import FundingProgram


class FundingProgramAdmin(admin.ModelAdmin):
    search_fields = ['full_name']
    list_display = ('full_name', 'organization', 'concession_year', 'geographical_scope')
    list_filter = ['concession_year', 'geographical_scope']

admin.site.register(FundingProgram, FundingProgramAdmin)
