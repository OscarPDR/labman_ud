# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import ZoteroExtractorLog


###     ZoteroExtractorLogAdmin
####################################################################################################

class ZoteroExtractorLogAdmin(admin.ModelAdmin):
    model = ZoteroExtractorLog

    list_display = ['item_key', 'version', 'timestamp', 'publication']
    search_fields = ['item_key', 'version', 'publication__title', 'publication__slug']


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(ZoteroExtractorLog, ZoteroExtractorLogAdmin)
