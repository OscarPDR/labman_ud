# coding: utf-8

from django.contrib import admin
from .models import Event, EventType, EventLogo, Viva, VivaPanel


#########################
# Class: EventLogoInline
#########################

class EventLogoInline(admin.TabularInline):
    model = EventLogo
    extra = 1


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
    inlines = [
        EventLogoInline,
    ]


#########################
# Class: VivaAdmin
#########################

class VivaAdmin(admin.ModelAdmin):
    model = Viva


#########################
# Class: VivaPanelAdmin
#########################

class VivaPanelAdmin(admin.ModelAdmin):
    model = VivaPanel


#########################
# Class: EventTypeAdmin
#########################

class EventTypeAdmin(admin.ModelAdmin):
    model = EventType
    exclude = [
        'slug',
    ]


##################################################
# Register classes
##################################################

admin.site.register(Event, EventAdmin)
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Viva, VivaAdmin)
admin.site.register(VivaPanel, VivaPanelAdmin)
