# Create your views here.

from django.shortcuts import render_to_response

def organization_list(request):
	return render_to_response('organization_manager/organization_list.html')