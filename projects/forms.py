# coding: utf-8

from django import forms
from django.forms import widgets
from django.forms.models import inlineformset_factory

from .models import Project, FundingAmount, AssignedEmployee, ConsortiumMember

# Create the form class.

FundingAmountFormSet = inlineformset_factory(Project, FundingAmount, extra=10)
AssignedEmployeeFormSet = inlineformset_factory(Project, AssignedEmployee, extra=1)
ConsortiumMemberFormSet = inlineformset_factory(Project, ConsortiumMember, extra=1)


#########################
# Widget: URLInput
#########################

class URLInput(widgets.Input):
    input_type = 'url'


#########################
# Class: ProjectSearchForm
#########################

class ProjectSearchForm(forms.Form):
    text = forms.CharField(max_length=50)


#########################
# Form: ProjectForm
#########################

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            'homepage': URLInput(attrs={'placeholder': 'http://'}),
        }
