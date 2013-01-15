
from django import forms
from django.forms import widgets
from django.forms.models import inlineformset_factory

from project_manager.models import *

# Create the form class.

class URLInput(widgets.Input):
    input_type = 'url'


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        widgets = {
            'homepage': URLInput(attrs={'placeholder': 'http://'}),
        }
        exclude = ('slug')
