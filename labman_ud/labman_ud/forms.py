
from django import forms
from django.contrib.auth.forms import AuthenticationForm


####################################################################################################
###     LoginForm
####################################################################################################

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
