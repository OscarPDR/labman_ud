
from django import forms


class TagRenameForm(forms.Form):
    tag_name = forms.CharField(max_length=100)
