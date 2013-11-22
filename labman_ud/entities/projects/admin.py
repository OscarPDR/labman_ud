# coding: utf-8

from django.contrib import admin

from .models import Project, ProjectType, ProjectLogo, Funding, FundingAmount, AssignedPerson, ConsortiumMember, RelatedPublication, ProjectTag


###########################################################################
# Class: FundingAmountInline
###########################################################################

class FundingAmountInline(admin.TabularInline):
    model = FundingAmount
    extra = 1


###########################################################################
# Class: ProjectTagInline
###########################################################################

class ProjectTagInline(admin.TabularInline):
    model = ProjectTag
    extra = 1


###########################################################################
# Class: FundingInline
###########################################################################

class FundingInline(admin.TabularInline):
    model = Funding
    extra = 1
    inlines = [
        FundingAmountInline,
    ]


###########################################################################
# Class: ProjectLogoInline
###########################################################################

class ProjectLogoInline(admin.TabularInline):
    model = ProjectLogo
    extra = 1


###########################################################################
# Class: ConsortiumMemberInline
###########################################################################

class ConsortiumMemberInline(admin.TabularInline):
    model = ConsortiumMember
    extra = 1


###########################################################################
# Class: AssignedPersonInline
###########################################################################

class AssignedPersonInline(admin.TabularInline):
    model = AssignedPerson
    extra = 1


###########################################################################
# Class: RelatedPublicationInline
###########################################################################

class RelatedPublicationInline(admin.TabularInline):
    model = RelatedPublication
    extra = 1


###########################################################################
# Class: ProjectAdmin
###########################################################################

class ProjectAdmin(admin.ModelAdmin):
    model = Project

    search_fields = ['full_name', 'short_name']
    list_display = ['full_name', 'short_name', 'start_year', 'end_year', 'status']
    list_filter = ['start_year', 'end_year', 'status']
    exclude = [
        'slug',
    ]
    inlines = [
        FundingInline,
        ConsortiumMemberInline,
        AssignedPersonInline,
        ProjectLogoInline,
        RelatedPublicationInline,
        ProjectTagInline,
    ]


###########################################################################
# Class: ProjectTypeAdmin
###########################################################################

class ProjectTypeAdmin(admin.ModelAdmin):
    model = ProjectType

    list_display = ['name', 'description']


###########################################################################
# Class: FundingAdmin
###########################################################################

class FundingAdmin(admin.ModelAdmin):
    model = Funding

    search_fields = ['project__short_name', 'funding_program__short_name']
    list_display = ['project', 'funding_program', 'project_code', 'total_funds']
    inlines = [
        FundingAmountInline,
    ]


###########################################################################
# Class: FundingAmountAdmin
###########################################################################

class FundingAmountAdmin(admin.ModelAdmin):
    model = FundingAmount

    search_fields = ['funding__project__slug']
    list_display = ['funding', 'own_amount', 'year']
    list_filter = ['year']


###########################################################################
# Class: ProjectTagAdmin
###########################################################################

class ProjectTagAdmin(admin.ModelAdmin):
    model = ProjectTag

    search_fields = ['project__slug', 'tag__slug']
    list_display = ['project', 'tag']
    list_filter = ['tag__name']


###########################################################################
# Class: AssignedPersonAdmin
###########################################################################

class AssignedPersonAdmin(admin.ModelAdmin):
    model = AssignedPerson

    search_fields = ['project__short_name', 'person__full_name']
    list_display = ['person', 'project', 'role']
    list_filter = ['role']


###########################################################################
# Class: ConsortiumMemberAdmin
###########################################################################

class ConsortiumMemberAdmin(admin.ModelAdmin):
    model = ConsortiumMember

    search_fields = ['project__short_name', 'organization__short_name', 'organization__full_name']
    list_display = ['project', 'organization']


###########################################################################
# Class: RelatedPublicationAdmin
###########################################################################

class RelatedPublicationAdmin(admin.ModelAdmin):
    model = RelatedPublication

    search_fields = ['project__short_name', 'publication__title']
    list_display = ['project', 'publication']


###########################################################################
###########################################################################
# Register classes
###########################################################################
###########################################################################

admin.site.register(AssignedPerson, AssignedPersonAdmin)
admin.site.register(ConsortiumMember, ConsortiumMemberAdmin)
admin.site.register(Funding, FundingAdmin)
admin.site.register(FundingAmount, FundingAmountAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectTag, ProjectTagAdmin)
admin.site.register(ProjectType, ProjectTypeAdmin)
admin.site.register(RelatedPublication, RelatedPublicationAdmin)
