# coding: utf-8

from django import forms
from django.forms import widgets

from organizations.models import Organization

# Create your forms here.


#########################
# Widget: URLInput
#########################

class URLInput(widgets.Input):
    input_type = 'url'


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
