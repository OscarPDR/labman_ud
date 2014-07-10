# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *


###########################################################################
# Class: PersonRelatedToEventAdmin
###########################################################################

class PersonRelatedToEventInline(admin.TabularInline):
    model = PersonRelatedToEvent
    extra = 1


###########################################################################
# Class: EventTypeAdmin
###########################################################################

class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    exclude = [
        'slug',
    ]


###########################################################################
# Class: EventAdmin
###########################################################################

class EventAdmin(admin.ModelAdmin):
    model = Event
    search_fields = ['full_name', 'short_name', 'location', 'year']
    list_display = ['short_name', 'full_name', 'year']
    list_filter = ['year']
    exclude = [
        'slug',
    ]
    inlines = [
        PersonRelatedToEventInline,
    ]


###########################################################################
# Class: VivaAdmin
###########################################################################

class VivaAdmin(admin.ModelAdmin):
    model = Viva


###########################################################################
# Class: VivaPanelAdmin
###########################################################################

class VivaPanelAdmin(admin.ModelAdmin):
    model = VivaPanel


###########################################################################
# Class: PersonRelatedToEventAdmin
###########################################################################

class PersonRelatedToEventAdmin(admin.ModelAdmin):
    model = PersonRelatedToEvent

    search_fields = ['person__full_name', 'event__full_name']
    list_display = ['person', 'event']


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Viva, VivaAdmin)
admin.site.register(VivaPanel, VivaPanelAdmin)
