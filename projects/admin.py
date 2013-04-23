# coding: utf-8

from django.contrib import admin
from .models import Project, FundingAmount, AssignedEmployee, ConsortiumMember


class ProjectAdmin(admin.ModelAdmin):
    search_fields = ['title']
    list_display = ['title', 'start_year', 'end_year', 'status', 'total_funds', 'total_funds_deusto']
    list_filter = ['start_year', 'end_year', 'status']


class FundingAmountAdmin(admin.ModelAdmin):
    search_fields = ['project__title']
    list_display = ['project', 'amount', 'year']
    list_filter = ['year']


class AssignedEmployeeAdmin(admin.ModelAdmin):
    search_fields = ['project__title']
    list_display = ['employee', 'project', 'role']
    list_filter = ['role']


class ConsortiumMemberAdmin(admin.ModelAdmin):
    search_fields = ['project__title']
    list_display = ['project', 'organization']

admin.site.register(Project, ProjectAdmin)
admin.site.register(FundingAmount, FundingAmountAdmin)
admin.site.register(AssignedEmployee, AssignedEmployeeAdmin)
admin.site.register(ConsortiumMember, ConsortiumMemberAdmin)
