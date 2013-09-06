# coding: utf-8

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
    search_fields = ['full_name',]
    list_display = ['full_name', 'email', ]
    list_filter = ['is_active']
    inlines = [
        AccountProfileInline,
        NicknameInline,
        JobInline,
    ]
    exclude = [
        'full_name',
        'slug',
    ]


#########################
# Class: AccountProfileAdmin
#########################

class AccountProfileAdmin(admin.ModelAdmin):
    model = AccountProfile


##################################################
# Register classes
##################################################

admin.site.register(Person, PersonAdmin)
admin.site.register(AccountProfile, AccountProfileAdmin)
