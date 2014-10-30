# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *


###########################################################################
# Class: NewsTagInline
###########################################################################

class NewsTagInline(admin.TabularInline):
    model = NewsTag
    extra = 1


###########################################################################
# Class: EventRelatedToNewsInline
###########################################################################

class EventRelatedToNewsInline(admin.TabularInline):
    model = EventRelatedToNews
    extra = 1


###########################################################################
# Class: ProjectRelatedToNewsInline
###########################################################################

class ProjectRelatedToNewsInline(admin.TabularInline):
    model = ProjectRelatedToNews
    extra = 1


###########################################################################
# Class: PersonRelatedToNewsInline
###########################################################################

class PersonRelatedToNewsInline(admin.TabularInline):
    model = PersonRelatedToNews
    extra = 1


###########################################################################
# Class: PublicationRelatedToNewsInline
###########################################################################

class PublicationRelatedToNewsInline(admin.TabularInline):
    model = PublicationRelatedToNews
    extra = 1


###########################################################################
# Class: NewAdmin
###########################################################################

class NewsAdmin(admin.ModelAdmin):
    model = News
    search_fields = ['title', 'content']
    list_display = ['title', 'created']
    exclude = [
        'slug',
    ]
    inlines = [
        NewsTagInline,
        EventRelatedToNewsInline,
        ProjectRelatedToNewsInline,
        PersonRelatedToNewsInline,
        PublicationRelatedToNewsInline,
    ]


###########################################################################
# Class: NewsTagAdmin
###########################################################################

class NewsTagAdmin(admin.ModelAdmin):
    model = NewsTag


###########################################################################
# Class: EventRelatedToNewsAdmin
###########################################################################

class EventRelatedToNewsAdmin(admin.ModelAdmin):
    model = EventRelatedToNews

    search_fields = ['event__full_name', 'news__title']
    list_display = ['event', 'news']


###########################################################################
# Class: ProjectRelatedToNewsAdmin
###########################################################################

class ProjectRelatedToNewsAdmin(admin.ModelAdmin):
    model = ProjectRelatedToNews

    search_fields = ['project__full_name', 'news__title']
    list_display = ['project', 'news']


###########################################################################
# Class: PersonRelatedToNewsAdmin
###########################################################################

class PersonRelatedToNewsAdmin(admin.ModelAdmin):
    model = PersonRelatedToNews

    search_fields = ['person__full_name', 'news__title']
    list_display = ['person', 'news']


###########################################################################
# Class: PublicationRelatedToNewsAdmin
###########################################################################

class PublicationRelatedToNewsAdmin(admin.ModelAdmin):
    model = PublicationRelatedToNews

    search_fields = ['publication__title', 'news__title']
    list_display = ['publication', 'news']


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(News, NewsAdmin)
admin.site.register(NewsTag, NewsTagAdmin)

admin.site.register(EventRelatedToNews, EventRelatedToNewsAdmin)
admin.site.register(ProjectRelatedToNews, ProjectRelatedToNewsAdmin)
admin.site.register(PersonRelatedToNews, PersonRelatedToNewsAdmin)
admin.site.register(PublicationRelatedToNews, PublicationRelatedToNewsAdmin)
