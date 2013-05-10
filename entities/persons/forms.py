# coding: utf-8

from django import forms
from django.forms import widgets

from .models import Person

# Create your forms here.


#########################
# Class: URLInput
#########################

class URLInput(widgets.Input):
    input_type = 'url'


#########################
# Class: PersonSearchForm
#########################

class PersonSearchForm(forms.Form):
    text = forms.CharField(max_length=50)


#########################
# Class: PersonForm
#########################

class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
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
                raise forms.ValidationError("You must provide the organization the Person belongs to.")
            else:
                pass

        return organization
