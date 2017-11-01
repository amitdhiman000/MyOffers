from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

from public.controls import MessageControl
from common.apputil import *

from pprint import pprint
# Create your views here.

def aboutus(request):
	data = {'title' : 'About us'}
	return App_Render(request, 'public/public_aboutus_1.html', data)

class ContactsView(TemplateView):
	def get(self, request):
		data = {'title' : 'Contacts'}
		data.update(csrf(request))
		return App_Render(request, 'public/public_contacts_1.html', data)

	def post(self, request):
		pprint(request.POST)
		error = None
		data = {'title' : 'Contacts'}
		control = MessageControl()
		if control.parseRequest(request) and control.validate():
			control.register()
		else:
			error = control.errors()

		if request.is_ajax():
			if error == None:
				data.update({'status': 204, 'message':'successfuly sent'})
			else:
				data.update({'status': 402, 'error': error})
			return JsonResponse(data)
		else:
			if error == None:
				return App_Render(request, 'public/public_contacts_sent_1.html', data)
			else:
				request.session['form_errors'] = control.errors()
				request.session['form_values'] = control.values()
			return App_Render(request, 'public/public_contacts_1.html', data)
