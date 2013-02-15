# coding: utf-8

from django import forms

from funding_programs.models import FundingProgram

# Create the form class.

#########################
# Form: FundingProgramForm
#########################


class FundingProgramForm(forms.ModelForm):
    class Meta:
        model = FundingProgram
        exclude = ('slug')
