# -*- encoding: utf-8 -*-

from django.contrib import admin
from .models import Person, AccountProfile, Nickname, Job


#########################
# Class: AccountProfileInline
#########################

class AccountProfileInline(admin.TabularInline):
    model = AccountProfile
    extra = 1


#########################
# Class: NicknameInline
#########################

class NicknameInline(admin.TabularInline):
    model = Nickname
    extra = 1

    exclude = ['slug']


#########################
# Class: JobInline
#########################

class JobInline(admin.StackedInline):
    model = Job
    extra = 1


#########################
# Class: PersonAdmin
#########################

class PersonAdmin(admin.ModelAdmin):
    model = Person
    search_fields = ['full_name', 'slug']
    list_display = ['full_name', 'email', 'is_active']
    list_filter = ['is_active']
    inlines = [
        AccountProfileInline,
        NicknameInline,
        JobInline,
    ]
    exclude = [
        'full_name',
        'slug',
        'safe_biography',
    ]


#########################
# Class: AccountProfileAdmin
#########################

class AccountProfileAdmin(admin.ModelAdmin):
    model = AccountProfile


#########################
# Class: NicknameAdmin
#########################

class NicknameAdmin(admin.ModelAdmin):
    model = Nickname

    search_fields = ['nickname', 'slug']
    list_display = ['nickname', 'slug']
    exclude = ['slug']


##################################################
# Register classes
##################################################

admin.site.register(Person, PersonAdmin)
admin.site.register(AccountProfile, AccountProfileAdmin)
admin.site.register(Nickname, NicknameAdmin)
