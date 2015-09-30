# -*- encoding: utf-8 -*-

from django import forms


###		PersonSearchForm()
####################################################################################################

class PersonSearchForm(forms.Form):
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Researcher name',
        })
    )
