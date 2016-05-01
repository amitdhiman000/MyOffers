from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from .control import OfferControl
from .models import Offer

from pprint import pprint

# Create your views here.

def offer_home(request):
	c = {'title':'Offers'}
	inst = Offer()
	offers = inst.get_all()
	pprint(offers)
	c.update({'offers_list': offers})
	return render(request, 'offer_home.html', c)

def offer_view(request):
	c = {'title':'View Offers'}
	return render(request, 'offer_view.html', c)

def offer_create_view(request):
	c = {'title': 'Create Offer'}

	if 'form_errors' in request.session:
		c['form_errors'] = request.session['form_errors']
		c['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	return render(request, 'offer_create.html', c)

def offer_create_submit(request):
	c = {'title':'Added Successfully'}

	if request.method == 'POST':
		image = request.FILES['image']
		offer_c = OfferControl(request.POST, request.FILES)
		if offer_c.validate():
			offer_c.register()
			return render(request, 'offer_added.html', c)
		else:
			request.session['form_errors'] = offer_c.get_errors()
			request.session['form_values'] = offer_c.get_values()
			return HttpResponseRedirect('/offer/create')

		return HttpResponse("Successfully Submitted!")
	else:
		return HttpResponseRedirect('/home/invalid-request')