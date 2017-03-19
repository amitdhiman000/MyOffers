from django.shortcuts import render
import device
# Create your views here.

def index(request):
	data = {'title': 'Error', 'page':'home'};
#	return HttpResponse ('This is Invalid Request')
	file = device.get_template(request, 'error_error.html')
	return render(request, file, data)

def access_denied_view(request):
	data = {'title': 'Access Denied', 'page': 'home'}
	file = device.get_template(request, 'error_access_denied.html')
	return render(request, file, data)

def invalid_request_view(request):
	data = {'title': 'Invalid Request', 'page':'home'};
	file = device.get_template(request, 'error_invalid_request.html')
	return render(request, file, data)

def under_construction_view(request):
	data = {'title': 'Under Construction', 'page':'home'};
	file = device.get_template(request, 'error_under_construction.html')
	return render(request, file, data)
