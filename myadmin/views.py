from django.conf import settings
from django.shortcuts import render
from myadmin.backenddb import add_default_values
from myadmin.backenddb import add_custom_values

from locus.models import Country
from locus.models import State
from locus.models import City
from locus.models import Area
from public.models import GuestMessage
from public.models import UserMessage

import device
from common import *
from common import __redirect
from myadmin.preload_locations import gStates
# Create your views here.

@admin_required
def home(request):
	data = {'title': 'MyAdmin'}
	file = device.get_template(request, 'admin_home.html')
	return render(request, file, data)


@admin_required
def locus_view(request):
	countries = Country.get_all()
	states = State.get_all('India')
	data = {'title': 'MyAdmin', 'countries': countries, 'states': states}
	file = device.get_template(request, 'admin_locus_view.html')
	return render(request, file, data)


@admin_required
def locus_area_view(request, country, state, city, area):
	areas = Area.get_area(country, state, city, area)
	data = {'title': 'MyAdmin', 'country': country, 'state': state, 'city':city, 'area':area, 'areas': areas}
	file = device.get_template(request, 'admin_locus_area.html')
	return render(request, file, data)


@admin_required
def locus_city_view(request, country, state, city):
	areas = Area.get_all(country, state, city)
	data = {'title': 'MyAdmin', 'country': country, 'state': state, 'city':city, 'areas': areas}
	file = device.get_template(request, 'admin_locus_city.html')
	return render(request, file, data)


@admin_required
def locus_state_view(request, country, state):
	cities = City.get_all(country, state)
	data = {'title': 'MyAdmin', 'country': country, 'state': state, 'cities':cities}
	file = device.get_template(request, 'admin_locus_state.html')
	return render(request, file, data)


@admin_required
def locus_country_view(request, country):
	states = State.get_all(country)
	data = {'title': 'MyAdmin', 'country': country, 'states': states}
	file = device.get_template(request, 'admin_locus_country.html')
	return render(request, file, data)


@admin_required
def locus_view1(request, query):
	print(query)
	params = query.split('/')
	length = len(params)
	print(len(params))
	if length == 1:
		return locus_country_view(request, params[0])
	elif length == 2:
		return locus_state_view(request, params[0], params[1])
	elif length == 3:
		return locus_city_view(request, params[0], params[1], params[2])
	elif length == 4:
		return locus_area_view(request, params[0], params[1], params[2], params[3])
	return locus_view(request)


@admin_required
def locus_add_view(request):
	countries = list(gStates.keys())
	data = {'title': 'MyAdmin', 'countries': countries}
	file = device.get_template(request, 'admin_locus_add.html')
	return render(request, file, data)


@admin_required
def locus_add_view1(request, country):
	states = {}
	if country in gStates:
		states = gStates[country]
	data = {'title': 'MyAdmin', 'country': country, 'states': states}
	file = device.get_template(request, 'admin_locus_add_country.html')
	return render(request, file, data)


@admin_required
def locus_auth(request, country, state, city):
	print(country, state, city)
	if City.get_by_name(city) == None:
		add_custom_values(state, city)
	areas = Area.get_by_city(city)
	data = {'title': 'Location', 'country':country, 'state': state, 'city': city, 'areas': areas}
	file = device.get_template(request, 'admin_locus_added.html')
	return render(request, file, data)


@admin_required
def messages_view(request):
	messages = GuestMessage.get_all()
	data = {'title': 'Messages', 'messages': messages}
	file = device.get_template(request, 'admin_message.html')
	return render(request, file, data)
