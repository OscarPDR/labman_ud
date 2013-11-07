# coding: utf-8

from django.contrib import admin

from .models import ZoteroLog

#########################
# Class: ZoteroLogAdmin
#########################

class ZoteroLogAdmin(admin.ModelAdmin):
    model = ZoteroLog
    list_display = ['zotero_key', 'delete', 'version', 'created', 'observations', 'publication']
    list_filter = ['zotero_key', 'delete', 'version', 'created']
    search_fields = ['zotero_key', 'version', 'publication__name']

admin.site.register(ZoteroLog, ZoteroLogAdmin)
