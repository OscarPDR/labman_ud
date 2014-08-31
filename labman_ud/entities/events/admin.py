# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *


###########################################################################
# Class: EventSeeAlsoInline
###########################################################################

class EventSeeAlsoInline(admin.TabularInline):
    model = EventSeeAlso
    extra = 1


###########################################################################
# Class: EventSeeAlsoAdmin
###########################################################################

class EventSeeAlsoAdmin(admin.ModelAdmin):
    model = EventSeeAlso

    list_display = ['event', 'see_also']
    search_fields = ['event__full_name']


###########################################################################
# Class: PersonRelatedToEventInline
###########################################################################

class PersonRelatedToEventInline(admin.TabularInline):
    model = PersonRelatedToEvent
    extra = 1


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
        EventSeeAlsoInline,
        PersonRelatedToEventInline,
    ]


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

admin.site.register(EventSeeAlso, EventSeeAlsoAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(PersonRelatedToEvent, PersonRelatedToEventAdmin)
