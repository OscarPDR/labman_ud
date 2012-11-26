
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from project_manager.models import *

# Create the form class.

class ProjectForm(forms.ModelForm):
	class Meta:
		model = Project