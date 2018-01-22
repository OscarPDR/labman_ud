# -*- encoding: utf-8 -*-

from django import forms
# from .models import *
from entities.utils.models import Tag, Role
from .choices import *


class CommaSeparatedStringField(forms.Field):

    def __init__(self, *args, **kwargs):
        self.token = kwargs.pop('token', ', ')
        super(CommaSeparatedStringField, self).__init__(*args, **kwargs)

    def to_python(self, value):
        if not value:
            return []
        if isinstance(value, list):
            return value
        return value.split(self.token)

    def clean(self, value):
        value = self.to_python(value)
        self.validate(value)
        self.run_validators(value)
        return value

###		DatasetSearchForm
####################################################################################################

class DatasetSearchForm(forms.Form):

    # Insert different labels for search engine
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Enter the name of Dataset',
        })
        , required=False)

    from_year = forms.CharField(
        max_length=4, required=False)

    from_range = forms.CharField(
        max_length=2, required=False)

    to_year = forms.CharField(
        max_length=4, required=False)

    to_range = forms.CharField(
        max_length=2, required=False)

    license = forms.MultipleChoiceField(choices=LICENSE_CHOICES,
                                label="License Type",
                                widget=forms.SelectMultiple(attrs={
                                 "class": "selectpicker",
                                 "multiple": "",
                                "data-width": "100%",
                                }),
                                help_text='Choose a license type of the dataset', required=False)

    file_format = forms.MultipleChoiceField(choices=FILE_FORMAT_CHOICES, label="File format",
                                    widget=forms.SelectMultiple(attrs={
                                        "class": "selectpicker",
                                        "multiple": "",
                                        "data-width": "100%",
                                    }),
                                    help_text="Choose a file extension", required=False,)

    tags = CommaSeparatedStringField(
        required=False)
