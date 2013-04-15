# coding: utf-8

from django.contrib import admin
from .models import Organization


class OrganizationAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['country']

admin.site.register(Organization, OrganizationAdmin)
