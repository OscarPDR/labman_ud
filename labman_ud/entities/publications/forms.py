# -*- encoding: utf-8 -*-

from django import forms


# Create your forms here.


###########################################################################
# Class: PublicationSearchForm
###########################################################################

class PublicationSearchForm(forms.Form):
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Publication title or author name',
        })
    )
