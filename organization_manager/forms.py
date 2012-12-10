# coding: utf-8

from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.forms import fields
from django.forms.models import inlineformset_factory

from organization_manager.models import *

# Create your forms here.

class URLInput(widgets.Input):
    input_type = 'url'

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        widgets = {
            'homepage': URLInput(attrs = {'placeholder': 'http://'}),
        }
        exclude = ('slug')