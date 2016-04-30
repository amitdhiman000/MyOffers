from django.shortcuts import render

# Create your views here.


def home_page(request):
	c = {'title': 'Home'}
	return render(request, 'home.html', c)

def invalid_request_view(request):
	c = {'title': 'Invalid request'}
	return render(request, 'invalid.html', c)

