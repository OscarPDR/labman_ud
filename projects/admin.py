# coding: utf-8

from django.contrib import admin
from nested_inlines.admin import NestedModelAdmin, NestedStackedInline, NestedTabularInline

from .models import Project, ProjectType, ProjectLogo, FundedProject, FundingAmount, AssignedPerson, ConsortiumMember


#########################
# Class: FundingAmountInline
#########################

class FundingAmountInline(NestedStackedInline):
    model = FundingAmount


#########################
# Class: FundedProjectInline
#########################

class FundedProjectInline(NestedStackedInline):
    model = FundedProject
    extra = 1
    inlines = [FundingAmountInline,]


#########################
# Class: ProjectLogoInline
#########################

class ProjectLogoInline(NestedStackedInline):
    model = ProjectLogo
    extra = 1


#########################
# Class: ConsortiumMemberInline
#########################

class ConsortiumMemberInline(NestedTabularInline):
    model = ConsortiumMember
    extra = 1


#########################
# Class: AssignedPersonInline
#########################

class AssignedPersonInline(NestedTabularInline):
    model = AssignedPerson
    extra = 1


#########################
# Class: ProjectAdmin
#########################

class ProjectAdmin(NestedModelAdmin):
    search_fields = ['full_name', 'short_name']
    list_display = ['full_name', 'short_name', 'start_year', 'end_year', 'status']
    list_filter = ['start_year', 'end_year', 'status']
    inlines = [
        FundedProjectInline,
        ConsortiumMemberInline,
        AssignedPersonInline,
        ProjectLogoInline,
    ]


#########################
# Class: ProjectTypeAdmin
#########################

class ProjectTypeAdmin(admin.ModelAdmin):
    model = ProjectType
    list_display = ['name', 'description']


#########################
# Class: FundedProjectAdmin
#########################

class FundedProjectAdmin(admin.ModelAdmin):
    search_fields = ['project__short_name', 'funding_program__short_name']
    list_display = ['project', 'funding_program', 'project_code', 'total_funds']
    inlines = [
        FundingAmountInline,
    ]


#########################
# Class: FundingAmountAdmin
#########################

class FundingAmountAdmin(admin.ModelAdmin):
    search_fields = ['funded_project__project__short_name']
    list_display = ['funded_project', 'consortium_amount', 'own_amount', 'year']
    list_filter = ['year']


#########################
# Class: AssignedPersonAdmin
#########################

class AssignedPersonAdmin(admin.ModelAdmin):
    search_fields = ['project__short_name', 'person__full_name']
    list_display = ['person', 'project', 'role']
    list_filter = ['role']


#########################
# Class: ConsortiumMemberAdmin
#########################

class ConsortiumMemberAdmin(admin.ModelAdmin):
    search_fields = ['project__short_name', 'organization__short_name', 'organization__full_name']
    list_display = ['project', 'organization']


##################################################
# Register classes
##################################################

admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectType, ProjectTypeAdmin)
admin.site.register(FundedProject, FundedProjectAdmin)
admin.site.register(FundingAmount, FundingAmountAdmin)
admin.site.register(AssignedPerson, AssignedPersonAdmin)
admin.site.register(ConsortiumMember, ConsortiumMemberAdmin)
