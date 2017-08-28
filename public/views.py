from django.shortcuts import render
from django.views.generic import TemplateView
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from public.control import MessageControl

from apputil import *
from apputil import __redirect
from apputil import __render
from apputil import __render as _renderview
from pprint import pprint
# Create your views here.

def aboutus(request):
	data = {'title' : 'About us'}
	return __render(request, 'public/public_aboutus_1.html', data)

class ContactsView(TemplateView):
	def get(self, request):
		data = {'title' : 'Contacts'}
		data.update(csrf(request))
		return _renderview(request, 'public/public_contacts_1.html', data)

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
				return renderview(request, 'public/public_contacts_sent_1.html', data)
			else:
				file = file = device.get_template(request, self.template_name)
				request.session['form_errors'] = control.get_errors()
				request.session['form_values'] = control.get_values()
			return renderview(request, 'public/public_contacts_1.html', data)
