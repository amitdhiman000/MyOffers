from django.conf import settings
from django.shortcuts import render
from myadmin.backenddb import add_default_values
from myadmin.backenddb import add_custom_values

from locus.models import Country
from locus.models import State
from locus.models import City
from locus.models import Area

import device
from common import *
from common import __redirect
# Create your views here.


gCities = (
	{'name': 'Andhra Pradesh', 'values': ['Hyderabad']},
	{'name': 'Chandigarh', 'values': ['Chandigarh']},
	{'name': 'Delhi', 'values': ['New Delhi', 'Central Delhi', 'East Delhi', 'North East Delhi', 'North West Delhi', 'South Delhi']},
	{'name': 'Himachal Pradesh', 'values': ['Shimla', 'Hamirpur(HP)']},
	{'name': 'Karnataka', 'values': ['Bangalore']},
	{'name': 'Maharashtra', 'values': ['Mumbai', 'Pune']},
	{'name': 'Tamil Nadu', 'values': ['Chennai', 'Coimbatore']}
)

@admin_required
def home(request):
	countries = Country.get_all()
	states = State.get_all('India')
	data = {'title': 'MyAdmin', 'countries': countries, 'states': states}
	file = device.get_template(request, 'admin_home.html')
	return render(request, file, data)

@admin_required
def locus_view(request):
	return home(request)

@admin_required
def locus_add_view(request):
	data = {'title': 'MyAdmin', 'states': gCities}
	file = device.get_template(request, 'admin_locus_add.html')
	return render(request, file, data)

@admin_required
def locus_auth(request, state, city):
	print(state)
	print(city)
	if City.get_by_name(city) == None:
		add_custom_values(state, city)

	areas = Area.get_by_city(city)
	data = {'title': 'Location', 'state': state, 'areas': areas}
	file = device.get_template(request, 'admin_locus_detail.html')
	return render(request, file, data)


@admin_required
def messages_view(request):
	data = {'title': 'Messages'}
	file = device.get_template(request, 'admin_message.html')
	return render(request, file, data)