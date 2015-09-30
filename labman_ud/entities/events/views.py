# -*- encoding: utf-8 -*-

from django.shortcuts import render

from django.conf import settings

from .models import Event

# Create your views here.

PAGINATION_NUMBER = settings.EVENTS_PAGINATION

###		event_index
####################################################################################################

def event_index(request):
    events = Event.objects.all()

    return_dict = {
        'events': events,
    }

    return render(request, "projects/index.html", return_dict)
