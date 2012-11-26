
from django import forms
from django.forms import ModelForm
from django.forms.models import inlineformset_factory

from employee_manager.models import *

# Create the form class.

class EmployeeForm(forms.ModelForm):
	class Meta:
		model = Employee