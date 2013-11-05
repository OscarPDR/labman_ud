# coding: utf-8

from django import forms

# Create the form class.


# #########################
# # Class: ProjectSearchForm
# #########################

class ProjectSearchForm(forms.Form):
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Project title or employee name',
        })
    )
