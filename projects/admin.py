# coding: utf-8

from django.contrib import admin
from .models import Project, FundingAmount, AssignedPerson, ConsortiumMember


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'short_name']
    list_display = ['full_name', 'short_name', 'start_year', 'end_year', 'status', 'total_funds']
    list_filter = ['start_year', 'end_year', 'status']


class FundingAmountAdmin(admin.ModelAdmin):
    search_fields = ['project__title']
    list_display = ['project', 'amount', 'year']
    list_filter = ['year']


class AssignedPersonAdmin(admin.ModelAdmin):
    search_fields = ['project__short_name']
    list_display = ['person', 'project', 'role']
    list_filter = ['role']


class ConsortiumMemberAdmin(admin.ModelAdmin):
    search_fields = ['project__short_name']
    list_display = ['project', 'organization']

admin.site.register(Project, ProjectAdmin)
admin.site.register(FundingAmount, FundingAmountAdmin)
admin.site.register(AssignedPerson, AssignedPersonAdmin)
admin.site.register(ConsortiumMember, ConsortiumMemberAdmin)
