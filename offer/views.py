from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .control import OfferControl
from .models import Offer

from common import login_required
import device

from pprint import pprint

# Create your views here.

def offer_home(request):
	offers = Offer.get_all()
	pprint(offers)
	obj = list(offers)
	pprint(obj[0].product_name)
	pprint(obj[0].discount)
	pprint(obj[0].start_date)
	data = {'title':'Offers', 'offers_list': offers}
	file = device.get_template(request, 'offer_home.html')
	return render(request, file, data)

def offer_view(request):
	data = {'title':'View Offers'}
	file = device.get_template(request, 'offer_view.html')
	return render(request, file, data)

def offer_create_view(request):
	data = {'title': 'Create Offer'}

	if 'form_errors' in request.session:
		c['form_errors'] = request.session['form_errors']
		c['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	file = device.get_template(request, 'offer_create.html')
	return render(request, file, data)

def offer_create_submit(request):
	data = {'title':'Added Successfully'}

	if request.method == 'POST':
		offer_c = OfferControl(request.POST)
		if offer_c.validate():
			offer_c.register()
			return render(request, 'offer_added.html', c)
		else:
			request.session['form_errors'] = offer_c.get_errors()
			request.session['form_values'] = offer_c.get_values()
			return HttpResponseRedirect('/offer/create')

		return HttpResponse("Successfully Submitted!")
	else:
		return HttpResponseRedirect(setting.ERROR_INVALID_REQUEST_URL)