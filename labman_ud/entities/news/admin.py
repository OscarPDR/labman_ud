# coding: utf-8

from django.contrib import admin
from .models import News, NewsTag, ProjectRelatedToNews, PersonRelatedToNews, PublicationRelatedToNews


#########################
# Class: NewsTagInline
#########################

class NewsTagInline(admin.TabularInline):
    model = NewsTag
    extra = 1


#########################
# Class: ProjectRelatedToNewsInline
#########################

class ProjectRelatedToNewsInline(admin.TabularInline):
    model = ProjectRelatedToNews
    extra = 1


#########################
# Class: PersonRelatedToNewsInline
#########################

class PersonRelatedToNewsInline(admin.TabularInline):
    model = PersonRelatedToNews
    extra = 1


#########################
# Class: PublicationRelatedToNewsInline
#########################

class PublicationRelatedToNewsInline(admin.TabularInline):
    model = PublicationRelatedToNews
    extra = 1


#########################
# Class: NewAdmin
#########################

class NewsAdmin(admin.ModelAdmin):
    model = News
    search_fields = ['title', 'text']
    list_display = ['title', 'created']
    exclude = [
        'slug',
    ]
    inlines = [
        NewsTagInline,
        ProjectRelatedToNewsInline,
        PersonRelatedToNewsInline,
        PublicationRelatedToNewsInline,
    ]


#########################
# Class: NewsTagAdmin
#########################

class NewsTagAdmin(admin.ModelAdmin):
    model = NewsTag


#########################
# Class: ProjectRelatedToNewsAdmin
#########################

class ProjectRelatedToNewsAdmin(admin.ModelAdmin):
    model = ProjectRelatedToNews


#########################
# Class: PersonRelatedToNewsAdmin
#########################

class PersonRelatedToNewsAdmin(admin.ModelAdmin):
    model = PersonRelatedToNews


#########################
# Class: PublicationRelatedToNewsAdmin
#########################

class PublicationRelatedToNewsAdmin(admin.ModelAdmin):
    model = PublicationRelatedToNews


##################################################
# Register classes
##################################################

admin.site.register(News, NewsAdmin)
admin.site.register(NewsTag, NewsTagAdmin)
