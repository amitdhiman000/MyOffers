from django.shortcuts import render
from apputil import App_Render
# Create your views here.

def index(request):
	data = {'title': 'Error', 'page':'home'};
#	return HttpResponse ('This is Invalid Request')
	return App_Render(request, 'error/error_error_1.html', data)

def access_denied_view(request):
	data = {'title': 'Access Denied', 'page': 'home'}
	return App_Render(request, 'error/error_access_denied_1.html', data)

def invalid_request_view(request):
	data = {'title': 'Invalid Request', 'page':'home'};
	return App_Render(request, 'error/error_invalid_request_1.html', data)

def under_construction_view(request):
	data = {'title': 'Under Construction', 'page':'home'};
	return App_Render(request, 'error/error_under_construction_1.html', data)
