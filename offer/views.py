import base64
from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta

from .models import Offer
from .control import OfferControl

from apputil import *
from apputil import App_Redirect
from apputil import App_Render
from pprint import pprint

# Create your views here.

def offer_home_view(request):
	offers = Offer.get_all()
	''''
	pprint(offers)
	obj = list(offers)
	'''
	data = {'title':'Offers', 'offers_list': offers}
	return App_Render(request, 'offer/offer_home_1.html', data)



def offer_detail_view(request, offer_id):
	print('offer_id : '+offer_id)
	offer = Offer.get_by_id(offer_id)
	data = {'title':'View Offers', 'offer': offer}
	return App_Render(request, 'offer/offer_detail_view_1.html', data)

def offer_detail_view1(request, slug):
	print('slug : '+slug)
	offer = Offer.get_by_slug(slug)
	data = {'title':'View Offers', 'offer': offer}
	return App_Render(request, 'offer/offer_detail_view_1.html', data)


@App_LoginRequired
def offer_create_view(request):
	pprint(request)
	imgdata = open(settings.STATIC_ROOT+"/images/icons-svg/location.svg", "rb").read()
	image = "data:image/svg+xml;base64,%s" % base64.b64encode(imgdata).decode('utf8')
	data = {'title': 'Create Offer', 'loc_image': image}
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']
	else:
		today = datetime.now().date()
		start = today.strftime("%Y/%m/%d")
		end = (today + timedelta(days=15)).strftime("%Y/%m/%d")
		data['form_values'] = {'P_start_date': start, 'P_expire_date': end}

	return App_Render(request, 'offer/offer_create_new_1.html', data)


@App_PostRequired
@App_LoginRequired
def offer_create(request):
	pprint(request)
	pprint(request.POST)
	data = {'title':'Added Successfully'}

	control = OfferControl()
	if control.parseRequest(request) and control.validate():
		control.register()
		#return App_Redirect(request, setting.OFFER_CREATE_SUCCESS)
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
