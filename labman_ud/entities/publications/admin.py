# coding: utf-8

from django.contrib import admin

from .models import *


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
# Class: ThesisAbstractInline
#########################

class ThesisAbstractInline(admin.TabularInline):
    model = ThesisAbstract
    extra = 1


#########################
# Class: CoAdvisorInline
#########################

class CoAdvisorInline(admin.TabularInline):
    model = CoAdvisor
    extra = 1


#########################
# Class: PublicationAdmin
#########################

class PublicationAdmin(admin.ModelAdmin):
    model = Publication

    search_fields = ['title', 'presented_at__short_name']
    list_display = ['title', 'publication_type', 'year', 'part_of']
    list_filter = ['publication_type__name', 'year']
    exclude = ['slug']
    inlines = [
        PublicationAuthorInline,
        PublicationTagInline,
    ]


#########################
# Class: ThesisAdmin
#########################

class ThesisAdmin(admin.ModelAdmin):
    model = Thesis

    search_fields = ['title', 'author__full_name']
    list_display = ['title', 'author', 'year']
    list_filter = ['year']
    exclude = ['slug']
    inlines = [
        ThesisAbstractInline,
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

    search_fields = ['publication__slug', 'author__slug']
    list_display = ['publication', 'author']
    list_filter = ['author__full_name']


#########################
# Class: PublicationTagAdmin
#########################

class PublicationTagAdmin(admin.ModelAdmin):
    model = PublicationTag

    search_fields = ['publication__slug', 'tag__slug']
    list_display = ['publication', 'tag']
    list_filter = ['tag__name']


#########################
# Class: ThesisAbstractAdmin
#########################

class ThesisAbstractAdmin(admin.ModelAdmin):
    model = ThesisAbstract


#########################
# Class: CoAdvisorAdmin
#########################

class CoAdvisorAdmin(admin.ModelAdmin):
    model = CoAdvisor


##################################################
# Register classes
##################################################

admin.site.register(CoAdvisor, CoAdvisorAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(PublicationAuthor, PublicationAuthorAdmin)
admin.site.register(PublicationTag, PublicationTagAdmin)
admin.site.register(PublicationType, PublicationTypeAdmin)
admin.site.register(Thesis, ThesisAdmin)
admin.site.register(ThesisAbstract, ThesisAbstractAdmin)
