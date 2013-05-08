# coding: utf-8

from django.contrib import admin
from .models import Event, EventLogo


class EventLogoInline(admin.TabularInline):
    model = EventLogo
    extra = 1


class EventAdmin(admin.ModelAdmin):
    search_fields = ['full_name', 'short_name', 'location', 'year']
    list_display = ['short_name', 'full_name', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [EventLogoInline]

admin.site.register(Event, EventAdmin)
