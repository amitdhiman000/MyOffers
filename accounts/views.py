from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#from django.contrib import auth
#from django.core.context_processors import csrf
from django.template.context_processors import csrf

#from django.template.loader import get_template
#from django.template import Context
from .control import ConsumerRegControl, VendorRegControl

## debugging
from pprint import pprint
## custom authentication class
from . import backends as auth


# Create your views here.

def login_old(request):
	c = {'title' : 'Login'};
	title = 'Login'
	t = get_template('login.html')
	html = t.render(Context({'title' : title}))
	return HttpResponse (html)


def login(request):
	c = {'title':'Login'}

	if 'form_errors' in request.session:
		c['form_errors'] = request.session['form_errors']
		c['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	c.update(csrf(request))
	return render(request,'login.html', c)


def auth1(request):
	if request.method == 'POST':
		username = request.POST.get('user', '')
		password = request.POST.get('pass', '')
		#user = auth.authenticate(username=username, password=password)
		user = auth.auth_consumer(username=username, password=password)

		if user is not None:
			pprint(vars(user))
			auth.login(request, user)
			#request.session.set_expiry(10)
			return HttpResponseRedirect('/accounts/loggedin')
		else:
			form_errors = {'user':'*Username or password is wrong!!'}
			form_values = {'user':request.POST.get('user', '')}
			request.session['form_errors'] = form_errors
			request.session['form_values'] = form_values
			return HttpResponseRedirect('/accounts/login')
	else:
		return HttpResponse('Invalid request!!')


def loggedin(request):
	c = {'title':'Profile'}
	return render(request, 'profile.html', c)


def profile(request):
	return loggedin(request)


def invalid(request):
	c = {'title': 'Invalid'};
#	return HttpResponse ('This is Invalid Request')
	return render(request, 'invalid.html', c)


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect('/')

#functions for registration
def signup(request):
	c = {'title':'Signup'}
	c.update(csrf(request))
	if 'form_errors' in request.session:
		c['form_errors'] = request.session['form_errors']
		c['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	return render(request,'signup.html', c)


def register(request):
	c = {'title':'Registration Successful'}
	if request.method == 'POST':
		control = None
		user_type = request.POST.get('user_type', '')
		if user_type == 'Consumer':
			control = ConsumerRegControl(request.POST)
		elif user_type == 'Vendor':
			control = VendorRegControl(request.POST)

		if control is not None:
			if control.validate():
				control.register()
				return render(request, 'registered.html', c)
			else:
				request.session['form_errors'] = control.get_errors()
				request.session['form_values'] = control.get_values()
				return HttpResponseRedirect('/accounts/signup')
	return HttpResponseRedirect('/accounts/invalid')
