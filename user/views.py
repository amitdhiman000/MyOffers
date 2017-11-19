from django.conf import settings
from django.shortcuts import render
from django.forms.models import model_to_dict
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

## custom authentication
from . import backends
from user.models import User
from locus.models import Address
from business.models import Category
from business.models import Business
from user.controls import *
from common.apputil import *

## debugging
from pprint import pprint
import logging
# Create your views here.


def home_view(request):
	return user_account_view(request)


@App_RedirectIfLoggedin
def signin_view(request):
	data = {'title':'Login'}
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	data.update(csrf(request))
	data.update({settings.USER_LOGIN_NEXT:request.GET.get(settings.USER_LOGIN_NEXT, '')})
	return App_Render(request, 'user/user_signin_1.html', data)



#functions for registration
@App_RedirectIfLoggedin
def signup_view(request):
	logging.debug('Hello');
	data = {'title':'Signup'}
	data.update(csrf(request))
	data.update({settings.USER_LOGIN_NEXT: request.POST.get(settings.USER_LOGIN_NEXT, '')})
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	return App_Render(request, 'user/user_signup_1.html', data)



@App_RedirectIfLoggedin
@App_PostRequired
def signin_auth(request):
	pprint(request.POST)
	control = UserSignInControl()
	if (control.parseRequest(request)
			and control.clean()
			and control.validate()):
		user = control.execute()
		if user != None:
			redirect_url = request.POST.get(settings.USER_LOGIN_NEXT, settings.HOME_URL)
			print('redirect amit : '+redirect_url)
			return App_Redirect(request, redirect_url)

	## Only error case will reach here.
	if request.is_ajax():
		error = control.errors()
		return JsonResponse({'status':401, 'message':'SignIn failed', 'data':error})
	else:
		redirect_url = request.META.get('HTTP_REFERER', settings.USER_LOGIN_URL)
		request.session['form_errors'] = control.errors()
		request.session['form_values'] = control.values()
		return App_Redirect(request, redirect_url)



@App_PostRequired
def signup_auth(request):
	pprint(request.POST)
	control = UserSignUpControl()
	if (control.parseRequest(request)
			and control.clean()
			and control.validate()):
		user = control.execute()
		if user != None:
			print('registration successful')
			backends.login(request, user)
			return App_Redirect(request, settings.USER_SIGNUP_SUCCESS_URL)

	error = control.errors()
	if request.is_ajax():
		return JsonResponse({'status':401, 'message': 'Signup Failed!!', 'data':error})
	else:
		request.session['form_errors'] = error
		request.session['form_values'] = control.values()
		return App_Redirect(request, settings.USER_SIGNUP_URL)



@App_LoginRequired
def signup_success_view(request):
	print('registration success')
	data = {'title':'Signup | Success'}
	return App_Render(request, 'user/user_registered_1.html', data)



def signout(request):
	backends.logout(request)
	return App_Redirect(request, settings.USER_LOGIN_URL)



@App_LoginRequired
def user_account_view(request):
	user = User.fetch_user(request.user)
	address = Address.fetch_by_user(user)
	user.address = address
	data = {'title':'Account', 'user': user}
	data.update(csrf(request))
	return App_Render(request, 'user/user_account_1.html', data)



@App_LoginRequired
def user_mails_view(request):
	print(request.GET.urlencode())
	data = {'title': 'User mails'}
	return App_Render(request, 'user/user_mails_1.html', data)



@App_LoginRequired
def user_stats_view(request):
	data = {'title': 'User stats'};
	return App_Render(request, 'user/user_stats_1.html', data)



@App_LoginRequired
def user_wishlist_view(request):
	data = {'title': 'User Wishlist'};
	return App_Render(request, 'user/user_wishlist_1.html', data)



@App_LoginRequired
def user_settings_view(request):
	data = {'title': 'User settings'};
	return App_Render(request, 'user/user_settings_1.html', data)



@App_LoginRequired
def user_update(request):
	data = None
	control = UserControlFactory.getControl(request)
	if (control.parseRequest(request)
			and control.clean()
			and control.validate()):
		data = control.execute()
		#pass

	if request.is_ajax:
		if data == None:
			return JsonResponse({'status': 400, 'message': 'Save Failed', 'data':control.errors()})
		else:
			return JsonResponse({'status': 200, 'message': 'Saved Successfully', 'data':data})
	else:
		return App_Redirect(request, '/user/account/')



@App_LoginRequired
def user_topic_selected(request):
	pprint(request.POST)
	error = None
	msg = None
	topic_id = request.POST.get('topic_id', -1)
	topic_followed = int(request.POST.get('topic_followed', 0))
	if topic_followed == 0:
		if TopicFollower.fetch_follower(request.user, topic_id):
			msg = 'folllowed'
		else:
			error = 'Server operation failed'
	elif topic_followed == 1:
		if TopicFollower.remove_follower(request.user, topic_id):
			msg = 'unfollowed'
		else:
			error = 'Server operation failed'
	else:
		error = 'Invalid request'

	## send the response
	if request.is_ajax():
		if error == None:
			return JsonResponse({'status':204, 'message': msg, 'data': {}})
		else:
			return JsonResponse({'status':401, 'message': 'Server Error', 'data': error})
	else:
		return App_Redirect(request, settings.HOME_PAGE_URL)
