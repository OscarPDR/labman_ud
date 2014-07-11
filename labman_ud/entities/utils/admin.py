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
# Class: LicenseAdmin
###########################################################################

class LicenseAdmin(admin.ModelAdmin):
    model = License


###########################################################################
# Class: FileItemAdmin
###########################################################################

class FileItemAdmin(admin.ModelAdmin):
    model = FileItem


###########################################################################
# Class: FileItemInline
###########################################################################

class FileItemInline(admin.TabularInline):
    model = FileItem
    extra = 1


###########################################################################
# Class: PersonRelatedToContributionInline
###########################################################################

class PersonRelatedToContributionInline(admin.TabularInline):
    model = PersonRelatedToContribution
    extra = 1


###########################################################################
# Class: PublicationRelatedToContributionInline
###########################################################################

class PublicationRelatedToContributionInline(admin.TabularInline):
    model = PublicationRelatedToContribution
    extra = 1


###########################################################################
# Class: ProjectRelatedToContributionInline
###########################################################################

class ProjectRelatedToContributionInline(admin.TabularInline):
    model = ProjectRelatedToContribution
    extra = 1


###########################################################################
# Class: TagRelatedToContributionInline
###########################################################################

class TagRelatedToContributionInline(admin.TabularInline):
    model = TagRelatedToContribution
    extra = 1


###########################################################################
# Class: FileItemRelatedToContributionInline
###########################################################################

class FileItemRelatedToContributionInline(admin.TabularInline):
    model = FileItemRelatedToContribution
    extra = 1


###########################################################################
# Class: ContributionTypeAdmin
###########################################################################

class ContributionTypeAdmin(admin.ModelAdmin):
    model = ContributionType


###########################################################################
# Class: ContributionAdmin
###########################################################################

class ContributionAdmin(admin.ModelAdmin):
    model = Contribution

    search_fields = ['title']
    list_display = ['title', 'contribution_type']
    exclude = [
        'slug',
    ]
    inlines = [
        FileItemRelatedToContributionInline,
        PersonRelatedToContributionInline,
        ProjectRelatedToContributionInline,
        PublicationRelatedToContributionInline,
        TagRelatedToContributionInline,
    ]


###########################################################################
# Class: PersonRelatedToTalkOrCourseInline
###########################################################################

class PersonRelatedToTalkOrCourseInline(admin.TabularInline):
    model = PersonRelatedToTalkOrCourse
    extra = 1


###########################################################################
# Class: ProjectRelatedToTalkOrCourseInline
###########################################################################

class ProjectRelatedToTalkOrCourseInline(admin.TabularInline):
    model = ProjectRelatedToTalkOrCourse
    extra = 1


###########################################################################
# Class: TagRelatedToTalkOrCourseInline
###########################################################################

class TagRelatedToTalkOrCourseInline(admin.TabularInline):
    model = TagRelatedToTalkOrCourse
    extra = 1


###########################################################################
# Class: FileItemRelatedToTalkOrCourseInline
###########################################################################

class FileItemRelatedToTalkOrCourseInline(admin.TabularInline):
    model = FileItemRelatedToTalkOrCourse
    extra = 1


###########################################################################
# Class: TalkOrCourseAdmin
###########################################################################

class TalkOrCourseAdmin(admin.ModelAdmin):
    model = TalkOrCourse

    search_fields = ['title']
    list_display = ['title', 'start_date', 'end_date']
    exclude = [
        'slug',
    ]
    inlines = [
        FileItemRelatedToTalkOrCourseInline,
        PersonRelatedToTalkOrCourseInline,
        ProjectRelatedToTalkOrCourseInline,
        TagRelatedToTalkOrCourseInline,
    ]


###########################################################################
# Class: PersonRelatedToAwardInline
###########################################################################

class PersonRelatedToAwardInline(admin.TabularInline):
    model = PersonRelatedToAward
    extra = 1


###########################################################################
# Class: ProjectRelatedToAwardInline
###########################################################################

class ProjectRelatedToAwardInline(admin.TabularInline):
    model = ProjectRelatedToAward
    extra = 1


###########################################################################
# Class: PublicationRelatedToAwardInline
###########################################################################

class PublicationRelatedToAwardInline(admin.TabularInline):
    model = PublicationRelatedToAward
    extra = 1


###########################################################################
# Class: AwardAdmin
###########################################################################

class AwardAdmin(admin.ModelAdmin):
    model = Award

    search_fields = ['full_name']
    list_display = ['full_name', 'date']
    exclude = [
        'slug',
    ]
    inlines = [
        PublicationRelatedToAwardInline,
        PersonRelatedToAwardInline,
        ProjectRelatedToAwardInline,
    ]


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
admin.site.register(FileItem, FileItemAdmin)
admin.site.register(License, LicenseAdmin)
admin.site.register(ContributionType, ContributionTypeAdmin)
admin.site.register(Contribution, ContributionAdmin)
admin.site.register(TalkOrCourse, TalkOrCourseAdmin)
admin.site.register(Award, AwardAdmin)
