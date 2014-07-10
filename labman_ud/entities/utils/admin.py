# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *


###########################################################################
# Class: CityAdmin
###########################################################################

class CityAdmin(admin.ModelAdmin):
    model = City

    search_fields = ['full_name', 'country']
    list_display = ['full_name']
    exclude = ['slug']


###########################################################################
# Class: CountryAdmin
###########################################################################

class CountryAdmin(admin.ModelAdmin):
    model = Country

    search_fields = ['full_name', 'short_name']
    list_display = ['full_name']
    exclude = ['slug']


###########################################################################
# Class: GeographicalScopeAdmin
###########################################################################

class GeographicalScopeAdmin(admin.ModelAdmin):
    model = GeographicalScope

    search_fields = ['name']
    list_display = ['name']
    exclude = ['slug']


###########################################################################
# Class: RoleAdmin
###########################################################################

class RoleAdmin(admin.ModelAdmin):
    model = Role

    search_fields = ['name']
    list_display = ['name']
    exclude = ['slug']


###########################################################################
# Class: TagAdmin
###########################################################################

class TagAdmin(admin.ModelAdmin):
    model = Tag

    search_fields = ['name']
    list_display = ['name', 'sub_tag_of']
    exclude = ['slug']


###########################################################################
# Class: LanguageAdmin
###########################################################################

class LanguageAdmin(admin.ModelAdmin):
    model = Language

    search_fields = ['name']
    list_display = ['name']
    exclude = ['slug']


###########################################################################
# Class: SocialNetworkAdmin
###########################################################################

class NetworkAdmin(admin.ModelAdmin):
    model = Network

    search_fields = ['name']
    list_display = ['name', 'base_url']
    exclude = ['slug']


###########################################################################
# Class: PhDProgramAdmin
###########################################################################

class PhDProgramAdmin(admin.ModelAdmin):
    model = PhDProgram


###########################################################################
###########################################################################
# Register classes
###########################################################################
###########################################################################

admin.site.register(City, CityAdmin)
admin.site.register(Country, CountryAdmin)
admin.site.register(GeographicalScope, GeographicalScopeAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Network, NetworkAdmin)
admin.site.register(PhDProgram, PhDProgramAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Tag, TagAdmin)
