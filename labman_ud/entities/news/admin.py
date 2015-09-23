# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *


###		NewsTagInline
####################################################################################################

class NewsTagInline(admin.TabularInline):
    model = NewsTag

    extra = 0


###		EventRelatedToNewsInline
####################################################################################################

class EventRelatedToNewsInline(admin.TabularInline):
    model = EventRelatedToNews

    extra = 0


###		ProjectRelatedToNewsInline
####################################################################################################

class ProjectRelatedToNewsInline(admin.TabularInline):
    model = ProjectRelatedToNews

    extra = 0


###		PersonRelatedToNewsInline
####################################################################################################

class PersonRelatedToNewsInline(admin.TabularInline):
    model = PersonRelatedToNews

    extra = 0


###		PublicationRelatedToNewsInline
####################################################################################################

class PublicationRelatedToNewsInline(admin.TabularInline):
    model = PublicationRelatedToNews

    extra = 0


###		NewAdmin
####################################################################################################

class NewsAdmin(admin.ModelAdmin):
    model = News

    search_fields = ['title', 'content']

    list_display = ['title', 'created']

    exclude = [
        'slug',
    ]

    inlines = [
        NewsTagInline,
        PersonRelatedToNewsInline,
        ProjectRelatedToNewsInline,
        PublicationRelatedToNewsInline,
        EventRelatedToNewsInline,
    ]


###		NewsTagAdmin
####################################################################################################

class NewsTagAdmin(admin.ModelAdmin):
    model = NewsTag

    search_fields = ['news__title', 'tag__name']

    list_display = ['news', 'tag']


###		EventRelatedToNewsAdmin
####################################################################################################

class EventRelatedToNewsAdmin(admin.ModelAdmin):
    model = EventRelatedToNews

    search_fields = ['event__full_name', 'news__title']

    list_display = ['event', 'news']


###		ProjectRelatedToNewsAdmin
####################################################################################################

class ProjectRelatedToNewsAdmin(admin.ModelAdmin):
    model = ProjectRelatedToNews

    search_fields = ['project__full_name', 'news__title']

    list_display = ['project', 'news']


###		PersonRelatedToNewsAdmin
####################################################################################################

class PersonRelatedToNewsAdmin(admin.ModelAdmin):
    model = PersonRelatedToNews

    search_fields = ['person__full_name', 'news__title']

    list_display = ['person', 'news']


###		PublicationRelatedToNewsAdmin
####################################################################################################

class PublicationRelatedToNewsAdmin(admin.ModelAdmin):
    model = PublicationRelatedToNews

    search_fields = ['publication__title', 'news__title']

    list_display = ['publication', 'news']


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################


admin.site.register(EventRelatedToNews, EventRelatedToNewsAdmin)
admin.site.register(News, NewsAdmin)
admin.site.register(NewsTag, NewsTagAdmin)
admin.site.register(PersonRelatedToNews, PersonRelatedToNewsAdmin)
admin.site.register(ProjectRelatedToNews, ProjectRelatedToNewsAdmin)
admin.site.register(PublicationRelatedToNews, PublicationRelatedToNewsAdmin)
