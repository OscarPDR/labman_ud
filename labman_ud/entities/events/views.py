# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.template.defaultfilters import slugify

from django.contrib.auth.decorators import login_required

from django.conf import settings

from email.mime.image import MIMEImage

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from .models import Event

from entities.projects.models import Project, FundingAmount, AssignedPerson, ConsortiumMember
from entities.projects.forms import ProjectForm, ProjectSearchForm, FundingAmountFormSet, AssignedPersonFormSet, ConsortiumMemberFormSet

from entities.persons.models import Person

from entities.organizations.models import Organization

from entities.funding_programs.models import FundingProgram

# Create your views here.

PAGINATION_NUMBER = settings.EVENTS_PAGINATION


#########################
# View: event_index
#########################

def event_index(request):
    events = Event.objects.all()

    return render_to_response("projects/index.html", {
            'events': events,
        },
        context_instance = RequestContext(request))
