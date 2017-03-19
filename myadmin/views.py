from django.conf import settings
from django.shortcuts import render
from .default_data import fill_default_values
from user.models import Country
from user.models import State
import device
from common import *
from common import __redirect
# Create your views here.


@admin_required
def home(request):
	if request.user.level != 9:
		__redirect(settings.ERROR_ACCESS_DENIED_URL)

	countries = Country.get_all()
	states = State.get_all('India')
	data = {'title': 'MyAdmin', 'countries': countries, 'states': states}
	file = device.get_template(request, 'admin_home.html')
	return render(request, file, data)

@admin_required
def fill_defaults(request):
	fill_default_values()
	return __redirect(request, settings.ADMIN_HOME)

@admin_required
def offer_create_view(request):
	return home(request)

@admin_required
def offer_create(request):
	return home(request)