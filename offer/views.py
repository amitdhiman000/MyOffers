import base64
from django.conf import settings
from django.http import (HttpResponse, JsonResponse, HttpResponseRedirect)
from django.views.decorators.csrf import (csrf_protect, csrf_exempt)
from datetime import (datetime, timedelta)

from business.models import Business
from offer.models import Offer
from offer.forms import (OfferRegForm, OfferUpdateForm, OfferDeleteForm)
from base.apputil import *


# Create your views here.

def offer_home_view(request):
	offers = Offer.fetch_all()
	data = {'title':'Offers', 'offers_list': offers}
	return App_Render(request, 'offer/offer_home_1.html', data)


def new1_view(request):
	return offer_form_view(request)


def online_view(request):
	return offer_home_view(request)


def nearby_view(request):
	return offer_home_view(request)


def bulk_view(request):
	return offer_home_view(request)


def food_view(request):
	return offer_home_view(request)


def offer_detail_view(request, slug):
	print('slug : '+slug)
	offer = Offer.fetch_by_slug(slug)
	data = {'title':'View Offers', 'offer': offer}
	return App_Render(request, 'offer/offer_item_detail_1.html', data)


@App_LoginRequired
def offer_form_view(request):
	print(request)
	businesses = Business.fetch_by_user(request.user)
	print(businesses)
	data = {'title': 'Create Offer', 'businesses': businesses}
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']
	else:
		today = datetime.now().date()
		start = today.strftime("%Y/%m/%d")
		end = (today + timedelta(days=15)).strftime("%Y/%m/%d")
		data['form_values'] = {'OF_start_date': start, 'OF_expire_date': end}

	return App_Render(request, 'offer/offer_create_form_1.html', data)


@App_LoginRequired
@App_PostRequired
def offer_create(request):
	print(request.POST)

	data = None
	form = OfferRegForm()
	if (form.parseForm(request)
		and form.clean()
		and form.validate()):
		data = form.commit()

	if request.is_ajax():
		if data != None:
			return JsonResponse({'status': 204, 'message': 'Offer created succesfuly'})
		else:
			return JsonResponse({'status': 401, 'message': 'Failed to create', 'data': form.errors()})
	else:
		if data != None:
			request.session['form_errors'] = form.errors()
			request.session['form_values'] = form.values()
		return HttpResponseRedirect(settings.OFFER_CREATE_NEW)


@App_LoginRequired
@App_PostRequired
def offer_update(request):
	print(request.POST)
	data = None
	form = OfferUpdateForm()
	if (form.parseForm(request)
		and form.clean()
		and form.validate()):
		data = form.commit()

	if request.is_ajax():
		if data != None:
			return JsonResponse({'status': 204, 'message': 'Offer updated succesfuly'})
		else:
			return JsonResponse({'status': 401, 'message': 'Failed to update', 'data': form.errors()})
	else:
		if data != None:
			request.session['form_errors'] = form.errors()
			request.session['form_values'] = form.values()
		return HttpResponseRedirect(settings.OFFER_CREATE_NEW)


@App_LoginRequired
@App_PostRequired
def offer_patch(request):
	print(request.POST)
	data = None
	form = OfferUpdateForm()
	if (form.parseForm(request)
		and form.clean()
		and form.validate()):
		data = form.commit()

	if request.is_ajax():
		if data != None:
			return JsonResponse({'status': 204, 'message': 'Offer updated succesfuly'})
		else:
			return JsonResponse({'status': 401, 'message': 'Failed to update', 'data': form.errors()})
	else:
		if data != None:
			request.session['form_errors'] = form.errors()
			request.session['form_values'] = form.values()
		return HttpResponseRedirect(settings.OFFER_CREATE_NEW)


@App_LoginRequired
@App_PostRequired
def offer_delete(request):
	print(request.POST)
	data = None
	form = OfferUpdateForm()
	if (form.parseForm(request)
		and form.clean()
		and form.validate()):
		data = form.commit()

	if request.is_ajax():
		if data != None:
			return JsonResponse({'status': 204, 'message': 'Offer deleted succesfuly'})
		else:
			return JsonResponse({'status': 401, 'message': 'Failed to delete', 'data': form.errors()})
	else:
		if data != None:
			request.session['form_errors'] = form.errors()
			request.session['form_values'] = form.values()
		return HttpResponseRedirect(settings.OFFER_CREATE_NEW)
