# -*- coding: utf-8 -*-

from django.contrib import admin

from .models import *


### Inline menus

###		NewsTagInline
####################################################################################################


class DatasetTagInline(admin.TabularInline):
    model = DatasetTag
    extra = 1

###		DatasetAuthorInline
####################################################################################################

class DatasetAuthorInline(admin.TabularInline):
    model = DatasetAuthor
    extra = 1

###		DatasetProjectInline
####################################################################################################

class DatasetProjectInline(admin.TabularInline):
    model = DatasetProject
    extra = 1

### Main registratopm of the admin entries

###		DatasetAdmin
####################################################################################################

@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    model = Dataset

    # Search fields
    search_fields = ['title', 'format']
    # What type of information we want to show in the admin list panel of datasets
    list_display = ['title', 'format', 'date']
    # Excluding some fields
    exclude = [
        'slug',
        'format'
    ]

    inlines = [
        DatasetTagInline,
        DatasetAuthorInline,
        DatasetProjectInline
    ]

###		DatasetTagAdmin
####################################################################################################

@admin.register(DatasetTag)
class DatasetTagAdmin(admin.ModelAdmin):
    model = DatasetTag

    search_fields = ['dataset__title', 'tag__name']
    list_display = ['dataset', 'tag']


###		DatasetAuthorAdmin
####################################################################################################

@admin.register(DatasetAuthor)
class DatasetAuthorAdmin(admin.ModelAdmin):
    model = DatasetAuthor

    search_fields = ['dataset__slug', 'author__slug']
    list_display = ['dataset', 'author', 'position']
    list_filter = ['author__full_name']


###		DatasetProjectAdmin
####################################################################################################

@admin.register(DatasetProject)
class DatasetProjectAdmin(admin.ModelAdmin):
    model = DatasetProject

    search_fields = ['dataset__title', 'project__short_name']
    list_display = ['dataset', 'project']
    list_filter = ['project__full_name']
