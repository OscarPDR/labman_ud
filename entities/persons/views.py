# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import Person
from .forms import PersonSearchForm

from entities.projects.models import Project, AssignedPerson

from entities.utils.models import Role

# Create your views here.

PAGINATION_NUMBER = settings.EMPLOYEES_PAGINATION


#########################
# View: person_index
#########################

def person_index(request):
    persons = Person.objects.all().order_by('full_name')

    if request.method == 'POST':
        form = PersonSearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['text']
            query = slugify(query)

            emps = []

            for person in persons:
                full_name = slugify(person.name + ' ' + person.first_surname + ' ' + person.second_surname)

                if query in full_name:
                    emps.append(person)

            persons = emps

    else:
        form = PersonSearchForm()

    paginator = Paginator(persons, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        persons = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        persons = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        persons = paginator.page(paginator.num_pages)

    return render_to_response("persons/index.html", {
            'persons': persons,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: person_info
#########################

def person_info(request, slug):
    person = get_object_or_404(Person, slug=slug)

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects['As: ' + role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=person.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('full_name')
        for project in project_objects:
            projects['As: ' + role.name].append(project)

    project_manager = Role.objects.get(name='Project Manager')

    apm = AssignedPerson.objects.filter(person_id=person.id, role=project_manager.id).values('project_id')
    as_project_manager = Project.objects.filter(id__in=apm).order_by('full_name')

    principal_researcher = Role.objects.get(name='Principal Researcher')

    apr = AssignedPerson.objects.filter(person_id=person.id, role=principal_researcher.id).values('project_id')
    as_principal_researcher = Project.objects.filter(id__in=apr).order_by('full_name')

    researcher = Role.objects.get(name='Researcher')

    ar = AssignedPerson.objects.filter(person_id=person.id, role=researcher.id).values('project_id')
    as_researcher = Project.objects.filter(id__in=ar).order_by('full_name')

    return render_to_response("persons/info.html", {
            'person': person,
            'projects': projects,
            'as_principal_researcher': as_principal_researcher,
            'as_project_manager': as_project_manager,
            'as_researcher': as_researcher,
        },
        context_instance=RequestContext(request))
