# coding: utf-8

from django import forms
from django.forms import widgets

from .models import Employee

# Create your forms here.


#########################
# Class: URLInput
#########################

class URLInput(widgets.Input):
    input_type = 'url'


#########################
# Class: EmployeeSearchForm
#########################

class EmployeeSearchForm(forms.Form):
    text = forms.CharField(max_length=50)


#########################
# Class: EmployeeForm
#########################

class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        widgets = {
            'foaf_link': URLInput(attrs={'placeholder': 'http://'}),
        }
        exclude = ('slug')

    def clean_organization(self):
        cleaned_data = self.cleaned_data
        external = cleaned_data.get('external')
        organization = cleaned_data.get('organization')

        if external:
            if organization is None:
                raise forms.ValidationError("You must provide the organization the employee belongs to.")
            else:
                pass

        return organization
