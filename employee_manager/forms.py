
from django import forms
from django.forms import ModelForm
from django.forms import widgets
from django.forms import fields
from django.forms.models import inlineformset_factory

from employee_manager.models import *

# Create the form class.

class URLInput(widgets.Input):
    input_type = 'url'

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        widgets = {
            'foaf_link': URLInput(attrs = {'placeholder': 'http://'}),
        }