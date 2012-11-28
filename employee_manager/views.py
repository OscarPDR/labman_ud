# Create your views here.

from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect

from employee_manager.models import *
from employee_manager.forms import *

def home(request):
	form = EmployeeForm()

	employees = Employee.objects.all()

	if request.POST:
		form = EmployeeForm(request.POST)
		if form.is_valid():
			return HttpResponseRedirect("/added")
	else:
		form = EmployeeForm()
	
	return render_to_response("index.html", {
			"form": form, 
			"employees": employees, 
		}, 
		context_instance = RequestContext(request))
