# coding: utf-8

from django import forms
from django.forms import widgets

from .models import Person


# Create your forms here.


#########################
# Class: PersonSearchForm
#########################

class PersonSearchForm(forms.Form):
    text = forms.CharField(max_length=50)
