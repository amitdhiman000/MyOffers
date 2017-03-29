from django.shortcuts import render
from offer.models import Offer
from offer.views import offer_home_view
##
from common import login_required
import device

from pprint import pprint
# Create your views here.

def home_page(request):
	return offer_home_view(request)

def home_backup(request):
	offers = Offer.get_all()
	data = {'title' : 'Contacts', 'offers_list': offers}
	file = device.get_template(request, 'home_backup.html')
	return render(request, file, data)

def aboutus(request):
	data = {'title' : 'About us'}
	file = device.get_template(request, 'home_aboutus.html')
	return render(request, file, data)


def contacts(request):
	data = {'title' : 'Contacts'}
	file = device.get_template(request, 'home_contacts.html')
	return render(request, file, data)


