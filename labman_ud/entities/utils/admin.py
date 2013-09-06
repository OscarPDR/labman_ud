# coding: utf-8

from django.contrib import admin
from .models import Country, GeographicalScope, Role, Tag, Language, Network


#########################
# Class: CountryAdmin
#########################

class CountryAdmin(admin.ModelAdmin):
    model = Country


#########################
# Class: GeographicalScopeAdmin
#########################

class GeographicalScopeAdmin(admin.ModelAdmin):
    model = GeographicalScope


#########################
# Class: RoleAdmin
#########################

class RoleAdmin(admin.ModelAdmin):
    model = Role


#########################
# Class: TagAdmin
#########################

class TagAdmin(admin.ModelAdmin):
    model = Tag


#########################
# Class: LanguageAdmin
#########################

class LanguageAdmin(admin.ModelAdmin):
    model = Language


#########################
# Class: SocialNetworkAdmin
#########################

class NetworkAdmin(admin.ModelAdmin):
    model = Network


##################################################
# Register classes
##################################################

admin.site.register(Country, CountryAdmin)
admin.site.register(GeographicalScope, GeographicalScopeAdmin)
admin.site.register(Role, RoleAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Language, LanguageAdmin)
admin.site.register(Network, NetworkAdmin)
