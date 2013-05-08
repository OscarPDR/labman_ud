# coding: utf-8

from django.contrib import admin
from .models import Publication, PublicationType


# class EventLogoInline(admin.TabularInline):
#     model = EventLogo
#     extra = 1


class PublicationAdmin(admin.ModelAdmin):
    search_fields = ['title', 'presented_at__short_name']
    list_display = ['title', 'publication_type', 'presented_at']
    list_filter = ['publication_type__name']
    exclude = ['slug']
    # inlines = [EventLogoInline]


class PublicationTypeAdmin(admin.ModelAdmin):
    model = PublicationType
    list_display = ['name', 'description']


admin.site.register(Publication, PublicationAdmin)
admin.site.register(PublicationType, PublicationTypeAdmin)
