# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import *


###########################################################################
# Class: PersonSeeAlsoInline
###########################################################################

class PersonSeeAlsoInline(admin.TabularInline):
    model = PersonSeeAlso
    extra = 1


###########################################################################
# Class: PersonSeeAlsoAdmin
###########################################################################

class PersonSeeAlsoAdmin(admin.ModelAdmin):
    model = PersonSeeAlso

    list_display = ['person', 'see_also']
    search_fields = ['person__full_name']

###########################################################################
# Class: AccountProfileInline
###########################################################################

class AccountProfileInline(admin.TabularInline):
    model = AccountProfile
    extra = 1


###########################################################################
# Class: NicknameInline
###########################################################################

class NicknameInline(admin.TabularInline):
    model = Nickname
    extra = 1

    exclude = ['slug']


###########################################################################
# Class: JobInline
###########################################################################

class JobInline(admin.StackedInline):
    model = Job
    extra = 1


###########################################################################
# Class: PersonAdmin
###########################################################################

class PersonAdmin(admin.ModelAdmin):
    model = Person
    search_fields = ['full_name', 'slug']
    list_display = ['full_name', 'email', 'is_active']
    list_filter = ['is_active']
    inlines = [
        PersonSeeAlsoInline,
        AccountProfileInline,
        NicknameInline,
        JobInline,
    ]
    exclude = [
        'full_name',
        'slug',
        'safe_biography',
    ]


###########################################################################
# Class: AccountProfileAdmin
###########################################################################

class AccountProfileAdmin(admin.ModelAdmin):
    model = AccountProfile


###########################################################################
# Class: NicknameAdmin
###########################################################################

class NicknameAdmin(admin.ModelAdmin):
    model = Nickname

    search_fields = ['nickname', 'slug']
    list_display = ['nickname', 'slug']
    exclude = ['slug']


####################################################################################################
####################################################################################################
###   Register classes
####################################################################################################
####################################################################################################

admin.site.register(PersonSeeAlso, PersonSeeAlsoAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(AccountProfile, AccountProfileAdmin)
admin.site.register(Nickname, NicknameAdmin)
