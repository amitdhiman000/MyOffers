from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from public.control import MessageControl

import device
from apputil import *
from apputil import __redirect
from pprint import pprint
# Create your views here.

def aboutus(request):
	data = {'title' : 'About us'}
	file = device.get_template(request, 'public/public_aboutus.html')
	return render(request, file, data)

class ContactsView(TemplateView):
	def get(self, request):
		data = {'title' : 'Contacts'}
		file = device.get_template(request, 'public/public_contacts.html')
		data.update(csrf(request))
		return render(request, file, data)

	def post(self, request):
		pprint(request.POST)
		error = None
		data = {'title' : 'Contacts'}
		control = MessageControl()
		if control.parseRequest(request) and control.validate():
			control.register()
		else:
			error = control.get_errors()

		if request.is_ajax():
			if error == None:
				data.update({'status': 204, 'message':'successfuly sent'})
			else:
				data.update({'status': 402, 'error': error})
			return JsonResponse(data)
		else:
			if error == None:
				file = device.get_template(request, 'public/public_contacts_sent.html')
			else:
				file = file = device.get_template(request, self.template_name)
				request.session['form_errors'] = control.get_errors()
				request.session['form_values'] = control.get_values()
			return render(request, file, data)
