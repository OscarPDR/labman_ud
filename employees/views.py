# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import Employee
from .forms import EmployeeForm, EmployeeSearchForm

from projects.models import Project, AssignedEmployee

# Create your views here.

PAGINATION_NUMBER = settings.EMPLOYEES_PAGINATION


#########################
# View: employee_index
#########################

def employee_index(request):
    employees = Employee.objects.all().order_by('name', 'first_surname', 'second_surname')

    if request.method == 'POST':
        form = EmployeeSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            emps = []

            for employee in employees:
                full_name = slugify(employee.name + ' ' + employee.first_surname + ' ' + employee.second_surname)

                if query in full_name:
                    emps.append(employee)

            employees = emps

    else:
        form = EmployeeSearchForm()

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

    return render_to_response("employees/index.html", {
            'employees': employees,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: add_employee
#########################

@login_required
def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            employee = Employee(
                name = cd['name'].encode('utf-8'),
                first_surname = cd['first_surname'].encode('utf-8'),
                second_surname = cd['second_surname'].encode('utf-8'),
                foaf_link = cd['foaf_link'],
                external = cd['external'],
                organization = cd['organization'],
            )

            employee.save()

            return HttpResponseRedirect(reverse('employee_index'))
    else:
        form = EmployeeForm()

    return render_to_response("employees/add.html", {
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: employee_info
#########################

def employee_info(request, slug):
    employee = get_object_or_404(Employee, slug = slug)

    apr = AssignedEmployee.objects.filter(employee_id = employee.id, role = 'Principal researcher').values('project_id')
    as_principal_researcher = Project.objects.filter(id__in = apr).order_by('title')

    apm = AssignedEmployee.objects.filter(employee_id = employee.id, role = 'Project manager').values('project_id')
    as_project_manager = Project.objects.filter(id__in = apm).order_by('title')

    ar = AssignedEmployee.objects.filter(employee_id = employee.id, role = 'Researcher').values('project_id')
    as_researcher = Project.objects.filter(id__in = ar).order_by('title')

    return render_to_response("employees/info.html", {
            'employee': employee,
            'as_principal_researcher': as_principal_researcher,
            'as_project_manager': as_project_manager,
            'as_researcher': as_researcher,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_employee
#########################

@login_required
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
            employee.external = cd['external']
            employee.organization = cd['organization']

            employee.save()

            return HttpResponseRedirect(reverse('employee_index'))

    else:
        data = {
            'name': employee.name,
            'first_surname': employee.first_surname,
            'second_surname': employee.second_surname,
            'foaf_link': employee.foaf_link,
            'external': employee.external,
            'organization': employee.organization,
        }

        form = EmployeeForm(initial = data)

    return render_to_response("employees/edit.html", {
            'employee': employee,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: delete_employee
#########################

@login_required
def delete_employee(request, slug):
    employee = get_object_or_404(Employee, slug = slug)
    employee.delete()

    return HttpResponseRedirect(reverse('employee_index'))
