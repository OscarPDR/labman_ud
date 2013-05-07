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
from .forms import PersonForm, PersonSearchForm

from projects.models import Project, AssignedPerson

# Create your views here.

PAGINATION_NUMBER = settings.EMPLOYEES_PAGINATION


#########################
# View: person_index
#########################

def person_index(request):
    persons = Person.objects.all().order_by('name', 'first_surname', 'second_surname')

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
# View: add_person
#########################

@login_required
def add_person(request):
    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            person = Person(
                name = cd['name'].encode('utf-8'),
                first_surname = cd['first_surname'].encode('utf-8'),
                second_surname = cd['second_surname'].encode('utf-8'),
                foaf_link = cd['foaf_link'],
                external = cd['external'],
                organization = cd['organization'],
            )

            person.save()

            return HttpResponseRedirect(reverse('person_index'))
    else:
        form = PersonForm()

    return render_to_response("persons/add.html", {
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: person_info
#########################

def person_info(request, slug):
    person = get_object_or_404(Person, slug = slug)

    apr = AssignedPerson.objects.filter(person_id = person.id, role = 'Principal researcher').values('project_id')
    as_principal_researcher = Project.objects.filter(id__in = apr).order_by('title')

    apm = AssignedPerson.objects.filter(person_id = person.id, role = 'Project manager').values('project_id')
    as_project_manager = Project.objects.filter(id__in = apm).order_by('title')

    ar = AssignedPerson.objects.filter(person_id = person.id, role = 'Researcher').values('project_id')
    as_researcher = Project.objects.filter(id__in = ar).order_by('title')

    return render_to_response("persons/info.html", {
            'person': person,
            'as_principal_researcher': as_principal_researcher,
            'as_project_manager': as_project_manager,
            'as_researcher': as_researcher,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_person
#########################

@login_required
def edit_person(request, slug):
    person = get_object_or_404(Person, slug = slug)

    if request.method == 'POST':
        form = PersonForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data

            person.name = cd['name'].encode('utf-8')
            person.first_surname = cd['first_surname'].encode('utf-8')
            person.second_surname = cd['second_surname'].encode('utf-8')
            person.foaf_link = cd['foaf_link']
            person.external = cd['external']
            person.organization = cd['organization']

            person.save()

            return HttpResponseRedirect(reverse('person_index'))

    else:
        data = {
            'name': person.name,
            'first_surname': person.first_surname,
            'second_surname': person.second_surname,
            'foaf_link': person.foaf_link,
            'external': person.external,
            'organization': person.organization,
        }

        form = PersonForm(initial = data)

    return render_to_response("persons/edit.html", {
            'person': person,
            'form': form,
        },
        context_instance = RequestContext(request))


#########################
# View: delete_person
#########################

@login_required
def delete_person(request, slug):
    person = get_object_or_404(Person, slug = slug)
    person.delete()

    return HttpResponseRedirect(reverse('person_index'))
