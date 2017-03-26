import base64
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .models import Offer
from .control import OfferControl

import device
from common import *
from common import __redirect
from pprint import pprint

# Create your views here.

def offer_home_view(request):
	offers = Offer.get_all()
	pprint(offers)
	obj = list(offers)
	data = {'title':'Offers', 'offers_list': offers}
	file = device.get_template(request, 'offer_home.html')
	return render(request, file, data)



def offer_detail_view(request, offer_id):
	print('offer_id : '+offer_id)
	offer = Offer.get_by_id(offer_id)
	data = {'title':'View Offers', 'offer': offer}
	file = device.get_template(request, 'offer_detail_view.html')
	return render(request, file, data)


@login_required
def offer_create_view(request):
	pprint(request)
	imgdata = open(settings.STATIC_ROOT+"/images/site-icons-svg/location.svg", "rb").read()
	image = "data:image/svg+xml;base64,%s" % base64.b64encode(imgdata).decode('utf8')
	data = {'title': 'Create Offer', 'loc_image': image}
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	file = device.get_template(request, 'offer_create_new.html')
	return render(request, file, data)


@post_required
@login_required
def offer_create(request):
	pprint(request)
	pprint(request.POST)
	data = {'title':'Added Successfully'}

	control = OfferControl()
	if control.parseRequest(request) and control.validate():
		control.register()
		#return __redirect(request, setting.OFFER_CREATE_SUCCESS)
		return JsonResponse({'status': 204, 'message': 'Offer posted succesfuly'})
	else:
		if request.is_ajax():
			return JsonResponse({'status': 401, 'error': control.get_errors()})
		else:
			request.session['form_errors'] = control.get_errors()
			request.session['form_values'] = control.get_values()
			return HttpResponseRedirect(settings.OFFER_CREATE_NEW)


def online_view(request):
	return offer_home_view(request)


def nearby_view(request):
	return offer_home_view(request)


def bulk_view(request):
	return offer_home_view(request)


def food_view(request):
	return offer_home_view(request)