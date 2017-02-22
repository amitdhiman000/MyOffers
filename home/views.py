from django.shortcuts import render

##
from common import login_required
import device

# Create your views here.

def home_page(request):
	data = {'title': 'Home'}
	file = device.get_template(request, 'home.html')
	return render(request, file, data)

@login_required
def profile(request):
	data = {'title' : 'Profile'}
	file = device.get_template(request, 'user_profile.html')
	return render(request, file, data)


def aboutus(request):
	data = {'title' : 'About us'}
	file = device.get_template(request, 'home_aboutus.html')
	return render(request, file, data)


def contacts(request):
	data = {'title' : 'Contacts'}
	file = device.get_template(request, 'home_contacts.html')
	return render(request, file, data)


