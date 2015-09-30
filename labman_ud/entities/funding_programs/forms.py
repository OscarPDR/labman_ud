# -*- encoding: utf-8 -*-

from django import forms

from .models import FundingProgram


###		FundingProgramSearchForm
####################################################################################################

class FundingProgramSearchForm(forms.Form):
    text = forms.CharField(max_length=50)


###		FundingProgramForm
####################################################################################################

class FundingProgramForm(forms.ModelForm):
    class Meta:
        model = FundingProgram
        exclude = ('slug',)
