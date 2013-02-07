# coding: utf-8

from django import forms

from funding_call_manager.models import FundingCall

# Create the form class.

#########################
# Form: FundingCallForm
#########################


class FundingCallForm(forms.ModelForm):
    class Meta:
        model = FundingCall
        exclude = ('slug')
