from django.shortcuts import render
from accounts.backends import login_required

# Create your views here.


def home_page(request):
	c = {'title': 'Home'}
	return render(request, 'home.html', c)

@login_required
def profile(request):
	c = {'title' : 'Profile'}
	return render(request, 'profile.html', c)


def aboutus(request):
	c = {'title' : 'About us'}
	return render(request, 'aboutus.html', c)


def contacts(request):
	c = {'title' : 'Contacts'}
	return render(request, 'contacts.html', c)


def invalid_request_view(request):
	c = {'title': 'Invalid request'}
	return render(request, 'invalid.html', c)

