# -*- encoding: utf-8 -*-

from django import forms


###		OrganizationSearchForm
####################################################################################################

class OrganizationSearchForm(forms.Form):
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Organization name',
        })
    )
