# Create your views here.

from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import HttpResponseRedirect

from employee_manager.models import *
from employee_manager.forms import *

def index(request):
    employees = Employee.objects.all()

    return render_to_response("employee_manager/index.html", {
            "employees": employees, 
        }, 
        context_instance = RequestContext(request))

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect("/added")
    else:
        form = EmployeeForm()
        
    return render_to_response("employee_manager/add.html", {
            "form": form,
        },
        context_instance = RequestContext(request))

def delete_employee(request, employeeID):
    e = get_object_or_404(Employee, pk = employeeID)
    e.delete()
    employees = Employee.objects.all()

    return render_to_response("employee_manager/index.html", {
            "employees": employees,
            "form": form,
        },
        context_instance = RequestContext(request))