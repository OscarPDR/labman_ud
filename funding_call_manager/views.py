# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.contrib.auth.decorators import login_required

from funding_call_manager.models import FundingCall
from funding_call_manager.forms import FundingCallForm

from project_manager.models import Project, FundingProgram

# Create your views here.

PAGINATION_NUMBER = 5


#########################
# View: funding_call_index
#########################

def funding_call_index(request):
    funding_calls = FundingCall.objects.all().order_by('full_name')
    paginator = Paginator(funding_calls, PAGINATION_NUMBER)

    page = request.GET.get('page')

    try:
        funding_calls = paginator.page(page)

    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        funding_calls = paginator.page(1)

    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        funding_calls = paginator.page(paginator.num_pages)
    return render_to_response("funding_call_manager/index.html", {
            "funding_calls": funding_calls,
        },
        context_instance = RequestContext(request))


#########################
# View: add_funding_call
#########################

@login_required
def add_funding_call(request):
    if request.method == 'POST':
        form = FundingCallForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            funding_call = FundingCall(
                organization = cd['organization'],
                full_name = cd['full_name'].encode('utf-8'),
                short_name = cd['short_name'].encode('utf-8'),
                concession_year = cd['concession_year'],
                geographical_scope = cd['geographical_scope'].encode('utf-8'),
            )

            try:
                funding_call.logo = request.FILES['logo']
            except:
                    pass

            funding_call.save()

            return HttpResponseRedirect(reverse('funding_call_index'))
    else:
        form = FundingCallForm()

    return render_to_response("funding_call_manager/add.html", {
            "form": form,
        },
        context_instance = RequestContext(request))


#########################
# View: info_funding_call
#########################

def info_funding_call(request, slug):
    funding_call = get_object_or_404(FundingCall, slug = slug)
    funding_programs = FundingProgram.objects.filter(funding_call_id = funding_call.id).values("project_id")
    projects = Project.objects.filter(id__in = funding_programs)

    return render_to_response("funding_call_manager/info.html", {
            "funding_call": funding_call,
            "projects": projects,
        },
        context_instance = RequestContext(request))


#########################
# View: edit_funding_call
#########################

def edit_funding_call(request, slug):
    funding_call = get_object_or_404(FundingCall, slug = slug)

    if request.method == 'POST':
        form = FundingCallForm(request.POST)
        if form.is_valid():

            cd = form.cleaned_data

            funding_call.organization = cd['organization']
            funding_call.full_name = cd['full_name'].encode('utf-8')
            funding_call.short_name = cd['short_name'].encode('utf-8')
            funding_call.concession_year = cd['concession_year']
            funding_call.geographical_scope = cd['geographical_scope'].encode('utf-8')

            try:
                funding_call.logo = request.FILES['logo']
            except:
                    pass

            funding_call.save()

            return HttpResponseRedirect(reverse('funding_call_index'))

    else:
        data = {
            'organization': funding_call.organization,
            'full_name': funding_call.full_name,
            'short_name': funding_call.short_name,
            'concession_year': funding_call.concession_year,
            'geographical_scope': funding_call.geographical_scope,
            'logo': funding_call.logo,
        }

        form = FundingCallForm(initial = data)

    return render_to_response("funding_call_manager/edit.html", {
            "form": form,
            "funding_call": funding_call,
        },
        context_instance = RequestContext(request))


#########################
# View: delete_funding_call
#########################

@login_required
def delete_funding_call(request, slug):
    funding_call = get_object_or_404(FundingCall, slug = slug)
    funding_call.delete()

    return HttpResponseRedirect(reverse('funding_call_index'))
