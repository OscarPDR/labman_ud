# coding: utf-8

from django import forms

from .models import FundingProgram

# Create the form class.


#########################
# Class: FundingProgramSearchForm
#########################

class FundingProgramSearchForm(forms.Form):
    text = forms.CharField(max_length=50)


#########################
# Form: FundingProgramForm
#########################

class FundingProgramForm(forms.ModelForm):
    class Meta:
        model = FundingProgram
        exclude = ('slug')
