# coding: utf-8

from django.shortcuts import render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from employee_manager.models import *
from employee_manager.forms import *

# Create your views here.

PAGINATION_NUMBER = 5


#########################
# View: employee_index
#########################

def employee_index(request):
    employees = Employee.objects.all()
    paginator = Paginator(employees, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        employees = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        employees = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        employees = paginator.page(paginator.num_pages)

    return render_to_response("employee_manager/index.html", {
            "employees": employees,
        },
        context_instance = RequestContext(request))


#########################
# View: add_employee
#########################

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data

            emp = Employee(
                name = cd['name'].encode('utf-8'),
                first_surname = cd['first_surname'].encode('utf-8'),
                second_surname = cd['second_surname'].encode('utf-8'),
                foaf_link = cd['foaf_link'],
            )

            emp.save()

            return HttpResponseRedirect("/employees")
    else:
        form = EmployeeForm()

    return render_to_response("employee_manager/add.html", {
            "form": form,
        },
        context_instance = RequestContext(request))


#########################
# View: info_employee
#########################

def info_employee(request, slug):
    employee = get_object_or_404(Employee, slug = slug)

    return render_to_response("employee_manager/info.html", {
            "employee": employee,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_employee
#########################

def edit_employee(request, slug):
    employee = get_object_or_404(Employee, slug = slug)

    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data

            employee.name = cd['name'].encode('utf-8')
            employee.first_surname = cd['first_surname'].encode('utf-8')
            employee.second_surname = cd['second_surname'].encode('utf-8')
            employee.foaf_link = cd['foaf_link']

            employee.save()

            return HttpResponseRedirect("/personas")

    else:
        data = {
            'name': employee.name,
            'first_surname': employee.first_surname,
            'second_surname': employee.second_surname,
            'foaf_link': employee.foaf_link
        }

        form = EmployeeForm(initial = data)

    return render_to_response("employee_manager/edit.html", {
            "employee": employee,
            "form": form,
        },
        context_instance = RequestContext(request))


#########################
# View: delete_employee
#########################

def delete_employee(request, slug):
    employee = get_object_or_404(Employee, slug = slug)
    employee.delete()

    return redirect('employee_index')
