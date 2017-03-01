from django.shortcuts import render
from offer.models import Offer
##
from common import login_required
import device

from pprint import pprint
# Create your views here.

def home_page(request):
	offers = Offer.get_all()
	pprint(offers)
	data = {'title':'home', 'offers_list': offers}
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


