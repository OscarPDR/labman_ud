# coding: utf-8

from django import forms
from django.forms import widgets

from .models import Organization

# Create your forms here.


#########################
# Widget: URLInput
#########################

class URLInput(widgets.Input):
    input_type = 'url'


#########################
# Class: FundingProgramSearchForm
#########################

class OrganizationSearchForm(forms.Form):
    text = forms.CharField(max_length=50)


#########################
# Form: OrganizationForm
#########################

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        widgets = {
            'homepage': URLInput(attrs = {'placeholder': 'http://'}),
        }
        exclude = ('slug')
