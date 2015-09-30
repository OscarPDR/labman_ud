# -*- encoding: utf-8 -*-

from django.contrib import admin

from .models import *

###		ProjectSeeAlsoInline
####################################################################################################

class ProjectSeeAlsoInline(admin.TabularInline):
    model = ProjectSeeAlso
    extra = 1

###		ProjectSeeAlsoAdmin
####################################################################################################

class ProjectSeeAlsoAdmin(admin.ModelAdmin):
    model = ProjectSeeAlso

    list_display = ['project', 'see_also']
    search_fields = ['project__full_name']

###		FundingSeeAlsoInline
####################################################################################################

class FundingSeeAlsoInline(admin.TabularInline):
    model = FundingSeeAlso
    extra = 1

###		FundingSeeAlsoAdmin
####################################################################################################

class FundingSeeAlsoAdmin(admin.ModelAdmin):
    model = FundingSeeAlso

    list_display = ['funding', 'see_also']
    search_fields = ['funding__slug']

###		FundingAmountInline
####################################################################################################

class FundingAmountInline(admin.TabularInline):
    model = FundingAmount
    extra = 1

###		ProjectTagInline
####################################################################################################

class ProjectTagInline(admin.TabularInline):
    model = ProjectTag
    extra = 1

###		FundingInline
####################################################################################################

class FundingInline(admin.TabularInline):
    model = Funding
    extra = 1
    inlines = [
        FundingSeeAlsoInline,
        FundingAmountInline,
    ]

    exclude = ['slug']

###		ConsortiumMemberInline
####################################################################################################

class ConsortiumMemberInline(admin.TabularInline):
    model = ConsortiumMember
    extra = 1

###		AssignedPersonInline
####################################################################################################

class AssignedPersonInline(admin.TabularInline):
    model = AssignedPerson
    extra = 1
    exclude = ['description']

###		RelatedPublicationInline
####################################################################################################

class RelatedPublicationInline(admin.TabularInline):
    model = RelatedPublication
    extra = 1

###		ProjectAdmin
####################################################################################################

class ProjectAdmin(admin.ModelAdmin):
    model = Project

    search_fields = ['full_name', 'short_name']
    list_display = ['full_name', 'short_name', 'start_year', 'end_year', 'status']
    list_filter = ['start_year', 'end_year', 'status', 'project_type']
    exclude = [
        'slug',
    ]
    inlines = [
        ProjectSeeAlsoInline,
        FundingInline,
        ConsortiumMemberInline,
        AssignedPersonInline,
        RelatedPublicationInline,
        ProjectTagInline,
    ]

###		FundingAdmin
####################################################################################################

class FundingAdmin(admin.ModelAdmin):
    model = Funding

    search_fields = ['project__short_name', 'funding_program__short_name']
    list_display = ['project', 'funding_program', 'project_code', 'total_funds']
    inlines = [
        FundingAmountInline,
    ]

###		FundingAmountAdmin
####################################################################################################

class FundingAmountAdmin(admin.ModelAdmin):
    model = FundingAmount

    search_fields = ['funding__project__slug']
    list_display = ['funding', 'own_amount', 'year']
    list_filter = ['year']

###		ProjectTagAdmin
####################################################################################################

class ProjectTagAdmin(admin.ModelAdmin):
    model = ProjectTag

    search_fields = ['project__slug', 'tag__slug']
    list_display = ['project', 'tag']
    list_filter = ['tag__name']

###		AssignedPersonAdmin
####################################################################################################

class AssignedPersonAdmin(admin.ModelAdmin):
    model = AssignedPerson

    search_fields = ['project__short_name', 'person__full_name']
    list_display = ['person', 'project', 'role']
    list_filter = ['role']

###		ConsortiumMemberAdmin
####################################################################################################

class ConsortiumMemberAdmin(admin.ModelAdmin):
    model = ConsortiumMember

    search_fields = ['project__short_name', 'organization__short_name', 'organization__full_name']
    list_display = ['project', 'organization']

###		RelatedPublicationAdmin
####################################################################################################

class RelatedPublicationAdmin(admin.ModelAdmin):
    model = RelatedPublication

    search_fields = ['project__short_name', 'publication__title']
    list_display = ['project', 'publication']


####################################################################################################
###########################################################################
# Register classes
####################################################################################################
###########################################################################

admin.site.register(ProjectSeeAlso, ProjectSeeAlsoAdmin)
admin.site.register(FundingSeeAlso, FundingSeeAlsoAdmin)
admin.site.register(AssignedPerson, AssignedPersonAdmin)
admin.site.register(ConsortiumMember, ConsortiumMemberAdmin)
admin.site.register(Funding, FundingAdmin)
admin.site.register(FundingAmount, FundingAmountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTag, ProjectTagAdmin)
admin.site.register(RelatedPublication, RelatedPublicationAdmin)
