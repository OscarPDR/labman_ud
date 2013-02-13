# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.db.models import Sum, Min, Max

from semantic_search.models import *
from semantic_search.forms import SemanticSearchForm

# Create your views here.


#########################
# View: semantic_search
#########################

def semantic_search(request):
    active = False
    title = ''
    researchers = ''
    status = 'Not started'
    scope = 'Euskadi'
    begin_year = 2004
    end_year = 2013
    and_or = 'OR'
    if request.method == 'POST':
        form = SemanticSearchForm(request.POST)
        if form.is_valid():
            active = True

            cd = form.cleaned_data

            title = cd['title']
            researchers = cd['researchers']
            status = cd['status']
            scope = cd['scope']
            begin_year = cd['begin_year']
            end_year = cd['end_year']
            and_or = cd['and_or']

    else:
        form = SemanticSearchForm()

    return render_to_response("semantic_search/searcher.html", {
            'active': active,
            'form': form,
            'title': title,
            'researchers': researchers,
            'status': status,
            'scope': scope,
            'begin_year': begin_year,
            'end_year': end_year,
            'and_or': and_or,
        },
        context_instance = RequestContext(request))


#########################
# View: query
#########################

def query(request):
    return render_to_response("semantic_search/searcher.html", {
        },
        context_instance = RequestContext(request))
