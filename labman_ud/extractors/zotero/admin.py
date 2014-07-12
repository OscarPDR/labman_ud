# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import ZoteroExtractorLog


###########################################################################
# Class: ZoteroExtractorLogAdmin
###########################################################################

class ZoteroExtractorLogAdmin(admin.ModelAdmin):
    model = ZoteroExtractorLog

    list_display = ['item_key', 'version', 'timestamp', 'publication']
    search_fields = ['zotero_key', 'version', 'publication__title', 'publication__slug']


admin.site.register(ZoteroExtractorLog, ZoteroExtractorLogAdmin)
