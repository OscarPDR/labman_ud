# coding: utf-8

from django.contrib import admin
from employees.models import Employee


class EmployeeAdmin(admin.ModelAdmin):
    list_filter = ['external']

admin.site.register(Employee, EmployeeAdmin)
