
from django import forms

from entities.utils.models import Tag


class TagRenameForm(forms.Form):
    tag_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'placeholder': 'Tag name',
        })
    )

    parent_tag = forms.ModelChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.Select(attrs={
            'class': 'form-control',
            'type': 'select',
        })
    )


class PublicationItemForm(forms.Form):
    item_key = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control input-sm',
            'type': 'text',
            'placeholder': 'item key',
        })
    )
