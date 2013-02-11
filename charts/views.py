# coding: utf-8

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext

from django.db.models import Sum

from django.contrib.auth.decorators import login_required

from employee_manager.models import *
from employee_manager.forms import *

from project_manager.models import *
from project_manager.forms import *

# Create your views here.


#########################
# View: chart_index
#########################

def chart_index(request):
    return render_to_response("charts/index.html", {
        },
        context_instance = RequestContext(request))


#########################
# View: incomes_by_year
#########################

def incomes_by_year(request):
    incomes = FundingAmount.objects.filter(year = 2011).aggregate(Sum('amount'))

    return render_to_response("charts/incomes_by_year.html", {
	    "incomes": incomes,
        },
        context_instance = RequestContext(request))
