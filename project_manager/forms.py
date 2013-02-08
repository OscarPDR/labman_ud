# coding: utf-8

from django import forms
from django.forms import widgets
from django.forms.models import inlineformset_factory

from project_manager.models import Project, FundingProgram, FundingAmount, AssignedEmployee, ConsortiumMember

# Create the form class.

FundingAmountFormSet = inlineformset_factory(Project, FundingAmount, extra = 10)
AssignedEmployeeFormSet = inlineformset_factory(Project, AssignedEmployee, extra = 1)
ConsortiumMemberFormSet = inlineformset_factory(Project, ConsortiumMember, extra = 1)


#########################
# Widget: URLInput
#########################

class URLInput(widgets.Input):
    input_type = 'url'


#########################
# Form: ProjectForm
#########################

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            'homepage': URLInput(attrs={'placeholder': 'http://'}),
        }


#########################
# Form: FundingProgramForm
#########################

class FundingProgramForm(forms.ModelForm):
    class Meta:
        model = FundingProgram
        exclude = ('project', 'slug')
