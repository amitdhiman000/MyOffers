from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from .control import OfferControl
from .models import Offer
import base64

import device
from common import login_required, post_required, __redirect

from pprint import pprint

# Create your views here.

def offer_home(request):
	offers = Offer.get_all()
	pprint(offers)
	obj = list(offers)
	'''
	pprint(obj[0].product_name)
	pprint(obj[0].discount)
	pprint(obj[0].start_date)
	'''
	data = {'title':'Offers', 'offers_list': offers}
	file = device.get_template(request, 'offer_home.html')
	return render(request, file, data)


def offer_view(request):
	data = {'title':'View Offers'}
	file = device.get_template(request, 'offer_view.html')
	return render(request, file, data)


def offer_create_view(request):
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


@csrf_exempt
@post_required
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
	return offer_home(request)


def nearby_view(request):
	return offer_home(request)


def bulk_view(request):
	return offer_home(request)


def food_view(request):
	return offer_home(request)