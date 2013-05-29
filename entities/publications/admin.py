# coding: utf-8

from django.contrib import admin
from .models import Publication, PublicationType, PublicationAuthor, PublicationTag


#########################
# Class: PublicationTagAdmin
#########################

class PublicationTagInline(admin.StackedInline):
    model = PublicationTag
    extra = 1


#########################
# Class: PublicationAuthorInline
#########################

class PublicationAuthorInline(admin.TabularInline):
    model = PublicationAuthor
    extra = 1


#########################
# Class: PublicationAdmin
#########################

class PublicationAdmin(admin.ModelAdmin):
    class Media:
        js = ('js/publications.js',)

    model = Publication

    search_fields = ['title', 'presented_at__short_name']
    list_display = ['title', 'publication_type', 'presented_at']
    list_filter = ['publication_type__name']
    exclude = ['slug']
    inlines = [
        PublicationAuthorInline,
        PublicationTagInline,
    ]


#########################
# Class: PublicationTypeAdmin
#########################

class PublicationTypeAdmin(admin.ModelAdmin):
    model = PublicationType
    list_display = ['name', 'description']


#########################
# Class: PublicationAuthorAdmin
#########################

class PublicationAuthorAdmin(admin.ModelAdmin):
    model = PublicationAuthor


#########################
# Class: PublicationTagAdmin
#########################

class PublicationTagAdmin(admin.ModelAdmin):
    model = PublicationTag
    extra = 1


##################################################
# Register classes
##################################################

admin.site.register(Publication, PublicationAdmin)
admin.site.register(PublicationType, PublicationTypeAdmin)
admin.site.register(PublicationAuthor, PublicationAuthorAdmin)
admin.site.register(PublicationTag, PublicationTagAdmin)
