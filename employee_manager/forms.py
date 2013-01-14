# coding: utf-8

from django import forms
from django.forms import widgets

from employee_manager.models import *

# Create your forms here.


class URLInput(widgets.Input):
    input_type = 'url'


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        widgets = {
            'foaf_link': URLInput(attrs={'placeholder': 'http://'}),
        }
        exclude = ('slug')


class JobForm(forms.ModelForm):
    class Meta:
        model = Job
