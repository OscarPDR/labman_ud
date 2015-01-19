
from django.contrib import admin

from .models import *


####################################################################################################
###     CitySeeAlsoInline
####################################################################################################

class CitySeeAlsoInline(admin.TabularInline):
    model = CitySeeAlso
    extra = 1


####################################################################################################
###     CitySeeAlsoAdmin
####################################################################################################

class CitySeeAlsoAdmin(admin.ModelAdmin):
    model = CitySeeAlso

    list_display = ['city', 'see_also']
    search_fields = ['city__full_name']


####################################################################################################
###     CountrySeeAlsoInline
####################################################################################################

class CountrySeeAlsoInline(admin.TabularInline):
    model = CountrySeeAlso
    extra = 1


####################################################################################################
###     CountrySeeAlsoAdmin
####################################################################################################

class CountrySeeAlsoAdmin(admin.ModelAdmin):
    model = CountrySeeAlso

    list_display = ['country', 'see_also']
    search_fields = ['country__full_name']


####################################################################################################
###     GeographicalScopeSeeAlsoInline
####################################################################################################

class GeographicalScopeSeeAlsoInline(admin.TabularInline):
    model = GeographicalScopeSeeAlso
    extra = 1


####################################################################################################
###     GeographicalScopeSeeAlsoAdmin
####################################################################################################

class GeographicalScopeSeeAlsoAdmin(admin.ModelAdmin):
    model = GeographicalScopeSeeAlso

    list_display = ['geographical_scope', 'see_also']
    search_fields = ['geographical_scope__name']


####################################################################################################
###     TagSeeAlsoInline
####################################################################################################

class TagSeeAlsoInline(admin.TabularInline):
    model = TagSeeAlso
    extra = 1


####################################################################################################
###     TagSeeAlsoAdmin
####################################################################################################

class TagSeeAlsoAdmin(admin.ModelAdmin):
    model = TagSeeAlso

    list_display = ['tag', 'see_also']
    search_fields = ['tag__name']


####################################################################################################
###     LanguageSeeAlsoInline
####################################################################################################

class LanguageSeeAlsoInline(admin.TabularInline):
    model = LanguageSeeAlso
    extra = 1


####################################################################################################
###     LanguageSeeAlsoAdmin
####################################################################################################

class LanguageSeeAlsoAdmin(admin.ModelAdmin):
    model = LanguageSeeAlso

    list_display = ['language', 'see_also']
    search_fields = ['language__name']


####################################################################################################
###     NetworkSeeAlsoInline
####################################################################################################

class NetworkSeeAlsoInline(admin.TabularInline):
    model = NetworkSeeAlso
    extra = 1


####################################################################################################
###     NetworkSeeAlsoAdmin
####################################################################################################

class NetworkSeeAlsoAdmin(admin.ModelAdmin):
    model = NetworkSeeAlso

    list_display = ['network', 'see_also']
    search_fields = ['network__name']


####################################################################################################
###     PhDProgramSeeAlsoInline
####################################################################################################

class PhDProgramSeeAlsoInline(admin.TabularInline):
    model = PhDProgramSeeAlso
    extra = 1


####################################################################################################
###     PhDProgramSeeAlsoAdmin
####################################################################################################

class PhDProgramSeeAlsoAdmin(admin.ModelAdmin):
    model = PhDProgramSeeAlso

    list_display = ['phd_program', 'see_also']
    search_fields = ['phd_program__name']


####################################################################################################
###     ContributionSeeAlsoInline
####################################################################################################

class ContributionSeeAlsoInline(admin.TabularInline):
    model = ContributionSeeAlso
    extra = 1


####################################################################################################
###     ContributionSeeAlsoAdmin
####################################################################################################

class ContributionSeeAlsoAdmin(admin.ModelAdmin):
    model = ContributionSeeAlso

    list_display = ['contribution', 'see_also']
    search_fields = ['contribution__title']


####################################################################################################
###     LicenseSeeAlsoInline
####################################################################################################

class LicenseSeeAlsoInline(admin.TabularInline):
    model = LicenseSeeAlso
    extra = 1


####################################################################################################
###     LicenseSeeAlsoAdmin
####################################################################################################

class LicenseSeeAlsoAdmin(admin.ModelAdmin):
    model = LicenseSeeAlso

    list_display = ['license', 'see_also']
    search_fields = ['license__full_name']


####################################################################################################
###     TalkOrCourseSeeAlsoInline
####################################################################################################

class TalkOrCourseSeeAlsoInline(admin.TabularInline):
    model = TalkOrCourseSeeAlso
    extra = 1


####################################################################################################
###     TalkOrCourseSeeAlsoAdmin
####################################################################################################

class TalkOrCourseSeeAlsoAdmin(admin.ModelAdmin):
    model = TalkOrCourseSeeAlso

    list_display = ['talk_or_course', 'see_also']
    search_fields = ['talk_or_course__title']


####################################################################################################
###     AwardSeeAlsoInline
####################################################################################################

class AwardSeeAlsoInline(admin.TabularInline):
    model = AwardSeeAlso
    extra = 1


####################################################################################################
###     AwardSeeAlsoAdmin
####################################################################################################

class AwardSeeAlsoAdmin(admin.ModelAdmin):
    model = AwardSeeAlso

    list_display = ['award', 'see_also']
    search_fields = ['award__full_name']


####################################################################################################
###     CityAdmin
####################################################################################################

class CityAdmin(admin.ModelAdmin):
    model = City

    search_fields = ['full_name', 'country']
    list_display = ['full_name']
    exclude = ['slug']


####################################################################################################
###     CountryAdmin
####################################################################################################

class CountryAdmin(admin.ModelAdmin):
    model = Country

    search_fields = ['full_name', 'short_name']
    list_display = ['full_name']
    exclude = ['slug']


####################################################################################################
###     GeographicalScopeAdmin
####################################################################################################

class GeographicalScopeAdmin(admin.ModelAdmin):
    model = GeographicalScope

    search_fields = ['name']
    list_display = ['name']
    exclude = ['slug']


####################################################################################################
###     RoleAdmin
####################################################################################################

class RoleAdmin(admin.ModelAdmin):
    model = Role

    search_fields = ['name']
    list_display = ['name', 'relevance_order', 'exclude_from_charts', 'rgb_color']
    exclude = ['slug']


####################################################################################################
###     TagAdmin
####################################################################################################

class TagAdmin(admin.ModelAdmin):
    model = Tag

    search_fields = ['name']
    list_display = ['name', 'sub_tag_of']
    exclude = ['slug']


####################################################################################################
###     LanguageAdmin
####################################################################################################

class LanguageAdmin(admin.ModelAdmin):
    model = Language

    search_fields = ['name']
    list_display = ['name']
    exclude = ['slug']


####################################################################################################
###     SocialNetworkAdmin
####################################################################################################

class NetworkAdmin(admin.ModelAdmin):
    model = Network

    search_fields = ['name']
    list_display = ['name', 'base_url']
    exclude = ['slug']


####################################################################################################
###     PhDProgramAdmin
####################################################################################################

class PhDProgramAdmin(admin.ModelAdmin):
    model = PhDProgram

    list_display = ['name', 'university', 'faculty']


####################################################################################################
###     LicenseAdmin
####################################################################################################

class LicenseAdmin(admin.ModelAdmin):
    model = License


####################################################################################################
###     FileItemAdmin
####################################################################################################

class FileItemAdmin(admin.ModelAdmin):
    model = FileItem


####################################################################################################
###     FileItemInline
####################################################################################################

class FileItemInline(admin.TabularInline):
    model = FileItem
    extra = 1


####################################################################################################
###     PersonRelatedToContributionInline
####################################################################################################

class PersonRelatedToContributionInline(admin.TabularInline):
    model = PersonRelatedToContribution
    extra = 1


####################################################################################################
###     PublicationRelatedToContributionInline
####################################################################################################

class PublicationRelatedToContributionInline(admin.TabularInline):
    model = PublicationRelatedToContribution
    extra = 1


####################################################################################################
###     ProjectRelatedToContributionInline
####################################################################################################

class ProjectRelatedToContributionInline(admin.TabularInline):
    model = ProjectRelatedToContribution
    extra = 1


####################################################################################################
###     TagRelatedToContributionInline
####################################################################################################

class TagRelatedToContributionInline(admin.TabularInline):
    model = TagRelatedToContribution
    extra = 1


####################################################################################################
###     FileItemRelatedToContributionInline
####################################################################################################

class FileItemRelatedToContributionInline(admin.TabularInline):
    model = FileItemRelatedToContribution
    extra = 1


####################################################################################################
###     ContributionTypeAdmin
####################################################################################################

class ContributionTypeAdmin(admin.ModelAdmin):
    model = ContributionType


####################################################################################################
###     ContributionAdmin
####################################################################################################

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


####################################################################################################
###     PersonRelatedToTalkOrCourseInline
####################################################################################################

class PersonRelatedToTalkOrCourseInline(admin.TabularInline):
    model = PersonRelatedToTalkOrCourse
    extra = 1


####################################################################################################
###     ProjectRelatedToTalkOrCourseInline
####################################################################################################

class ProjectRelatedToTalkOrCourseInline(admin.TabularInline):
    model = ProjectRelatedToTalkOrCourse
    extra = 1


####################################################################################################
###     TagRelatedToTalkOrCourseInline
####################################################################################################

class TagRelatedToTalkOrCourseInline(admin.TabularInline):
    model = TagRelatedToTalkOrCourse
    extra = 1


####################################################################################################
###     FileItemRelatedToTalkOrCourseInline
####################################################################################################

class FileItemRelatedToTalkOrCourseInline(admin.TabularInline):
    model = FileItemRelatedToTalkOrCourse
    extra = 1


####################################################################################################
###     TalkOrCourseAdmin
####################################################################################################

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


####################################################################################################
###     PersonRelatedToAwardInline
####################################################################################################

class PersonRelatedToAwardInline(admin.TabularInline):
    model = PersonRelatedToAward
    extra = 1


####################################################################################################
###     ProjectRelatedToAwardInline
####################################################################################################

class ProjectRelatedToAwardInline(admin.TabularInline):
    model = ProjectRelatedToAward
    extra = 1


####################################################################################################
###     PublicationRelatedToAwardInline
####################################################################################################

class PublicationRelatedToAwardInline(admin.TabularInline):
    model = PublicationRelatedToAward
    extra = 1


####################################################################################################
###     AwardAdmin
####################################################################################################

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


####################################################################################################
####################################################################################################
###     Register classes
####################################################################################################
####################################################################################################


admin.site.register(CitySeeAlso, CitySeeAlsoAdmin)
admin.site.register(CountrySeeAlso, CountrySeeAlsoAdmin)
admin.site.register(GeographicalScopeSeeAlso, GeographicalScopeSeeAlsoAdmin)
admin.site.register(TagSeeAlso, TagSeeAlsoAdmin)
admin.site.register(LanguageSeeAlso, LanguageSeeAlsoAdmin)
admin.site.register(NetworkSeeAlso, NetworkSeeAlsoAdmin)
admin.site.register(PhDProgramSeeAlso, PhDProgramSeeAlsoAdmin)
admin.site.register(ContributionSeeAlso, ContributionSeeAlsoAdmin)
admin.site.register(LicenseSeeAlso, LicenseSeeAlsoAdmin)
admin.site.register(TalkOrCourseSeeAlso, TalkOrCourseSeeAlsoAdmin)
admin.site.register(AwardSeeAlso, AwardSeeAlsoAdmin)

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
