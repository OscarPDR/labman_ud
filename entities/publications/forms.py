# coding: utf-8

from django import forms


# Create your forms here.


#########################
# Class: PublicationSearchForm
#########################

class PublicationSearchForm(forms.Form):
    text = forms.CharField(max_length=50)
