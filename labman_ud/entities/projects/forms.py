# coding: utf-8

from django import forms

# Create the form class.


# #########################
# # Class: ProjectSearchForm
# #########################

class ProjectSearchForm(forms.Form):
    text = forms.CharField(max_length=50)
