# -*- encoding: utf-8 -*-

from django import forms
from django.contrib.auth.forms import AuthenticationForm


# Create the form class.


###########################################################################
# Class: LoginForm
###########################################################################

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'username',
        })
    )
    password = forms.CharField(
        max_length=50,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'placeholder': 'password',
        })
    )
