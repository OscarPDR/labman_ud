# -*- encoding: utf-8 -*-

from django import forms
from entities.utils.models import Tag
from entities.publications.models import Publication

PUBLICATION_TYPES = (())
types = Publication.objects.all().values_list('child_type', flat=True).order_by('child_type').distinct()
for choice in types:
    PUBLICATION_TYPES = PUBLICATION_TYPES + ((choice, choice),)


# Create your forms here.

###		PublicationSearchForm
####################################################################################################

class PublicationSearchForm(forms.Form):
    text = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Publication title or author name',
        })
    , required=False)

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)

    from_year = forms.CharField(
        max_length=4, required=False)

    from_range = forms.CharField(
        max_length=2, required=False)

    to_year = forms.CharField(
        max_length=4, required=False)

    to_range = forms.CharField(
        max_length=2, required=False)

    publication_types = forms.MultipleChoiceField(
        choices=PUBLICATION_TYPES, required=False)

    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(), required=False)

    author_field_count = forms.CharField(widget=forms.HiddenInput())
    editor_field_count = forms.CharField(widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        extra_editor_fields = kwargs.pop('extra_editor', 1)
        extra_author_fields = kwargs.pop('extra_author', 1)

        super(PublicationSearchForm, self).__init__(*args, **kwargs)
        self.fields['editor_field_count'].initial = extra_editor_fields
        self.fields['author_field_count'].initial = extra_author_fields

        for index in range(int(extra_editor_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['editor_name_{index}'.format(index=index + 1)] = forms.CharField(
                required=False)

        for index in range(int(extra_author_fields)):
            # generate extra fields in the number specified via extra_fields
            self.fields['author_name_{index}'.format(index=index + 1)] = forms.CharField(
                required=False)
