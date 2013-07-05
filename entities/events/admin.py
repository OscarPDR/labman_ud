# coding: utf-8

from django.contrib import admin
from .models import Event, EventType

#########################
# Class: EventTypeAdmin
#########################

class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    exclude = [
        'slug',
    ]

#########################
# Class: EventAdmin
#########################

class EventAdmin(admin.ModelAdmin):
    model = Event
    search_fields = ['full_name', 'short_name', 'location', 'year']
    list_display = ['short_name', 'full_name', 'year']
    list_filter = ['year']
    exclude = [
        'slug',
    ]

##################################################
# Register classes
##################################################

admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
