# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.conf import settings

from django.contrib.auth.decorators import login_required

from .models import Person, Job
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
                if query in person.slug:
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
# View: members
#########################

def members(request):

    members = []

    member_list = Person.objects.filter(is_active=True)

    for member in member_list:
        # job = Job.objects.get(person_id=member.id, end_date=None)
        members.append({
            "title": member.title,
            "full_name": member.full_name,
            # "position": job.position,
            "profile_picture_url": member.profile_picture,
             "slug": member.slug
        })

    return render_to_response("members/index.html", {
            'members': members,
        },
        context_instance=RequestContext(request))


#########################
# View: member_info
#########################

def member_info(request, member_slug):

    member = Person.objects.get(slug=member_slug)

    try:
        job = Job.objects.get(person_id=member.id, end_date=None)
        position = job.position
    except:
        job = None
        position = None

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=member.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('-start_year').order_by('-end_year')
        for project in project_objects:
            projects[role.name].append(project)

    return render_to_response("members/info.html", {
            'member': member,
            'position': position,
            'projects': projects,
        },
        context_instance=RequestContext(request))

#########################
# View: person_info
#########################

def person_info(request, slug):
    from_page = ''

    http_referer = request.META['HTTP_REFERER']

    if '?page=' in http_referer:
        from_page = http_referer[http_referer.rfind('/')+1:]

    person = get_object_or_404(Person, slug=slug)

    projects = {}

    roles = Role.objects.all()

    for role in roles:
        projects[role.name] = []
        project_ids = AssignedPerson.objects.filter(person_id=person.id, role=role.id).values('project_id')
        project_objects = Project.objects.filter(id__in=project_ids).order_by('slug')
        for project in project_objects:
            projects[role.name].append(project)

    return render_to_response("persons/info.html", {
            'person': person,
            'projects': projects,
            'from_page': from_page,
        },
        context_instance=RequestContext(request))
