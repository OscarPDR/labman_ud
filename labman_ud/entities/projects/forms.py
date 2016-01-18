# -*- encoding: utf-8 -*-

from django import forms
from .models import *
from entities.utils.models import Tag, Role

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

# Create the form class.

###		ProjectSearchForm
####################################################################################################

class ProjectSearchForm(forms.Form):
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Project title or researcher name',
        }), required=False
    )

    start_date = forms.CharField(
        max_length=7, required=False)

    start_range = forms.CharField(
        max_length=2, required=False)

    end_date = forms.CharField(
        max_length=7, required=False)

    end_range = forms.CharField(
        max_length=2, required=False)

    project_types = forms.MultipleChoiceField(
        choices=PROJECT_TYPES, required=False)

    status = forms.MultipleChoiceField(
        choices=PROJECT_STATUS, required=False)

    from_total_funds = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False)

    to_total_funds = forms.DecimalField(
        max_digits=10, decimal_places=2, required=False)

    funds_range = forms.CharField(
        max_length=2, required=False)

    tags = CommaSeparatedStringField(
        required=False)

    member_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_fields = kwargs.pop('extra', 1)

        super(ProjectSearchForm, self).__init__(*args, **kwargs)
        self.fields['member_field_count'].initial = extra_fields

        for index in range(int(extra_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['participant_role_{index}'.format(index=index + 1)] = forms.ModelMultipleChoiceField(
                queryset=Role.objects.all(), required=False)
            self.fields['participant_name_{index}'.format(index=index + 1)] = forms.CharField(
                required=False)
