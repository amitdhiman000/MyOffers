from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers

## custom packages
import device
from common import *
from common import __redirect
## custom authentication
from . import backends
from .models import User
from .control import UserRegControl
from .control import UserSignInControl

## debugging
from pprint import pprint
# Create your views here.

@redirect_if_loggedin
def signin_view(request):
	data = {'title':'Login', 'page':'user'}
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	data.update(csrf(request))
	file = device.get_template(request, 'user_signin.html')
	return render(request, file, data)


#functions for registration
def signup_view(request):
	data = {'title':'Signup', 'page':'user'}
	data.update(csrf(request))
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	file = device.get_template(request, 'user_signup.html')
	return render(request, file, data)


def signout(request):
	backends.logout(request)
	return __redirect(request, settings.USER_LOGIN_URL)


@post_required
def signin_auth(request):
	pprint(request.POST)
	error = None
	control = UserSignInControl()
	if control.parseRequest(request.POST) and control.signin(request):
		return __redirect(request, settings.USER_PROFILE_URL)	

	## Only error case will reach here.
	if request.is_ajax():
		error = control.get_errors()
		return JsonResponse({'status':401, 'error':error})
	else:
		request.session['form_errors'] = control.get_values()
		request.session['form_values'] = control.get_values()
		return __redirect(request, settings.USER_LOGIN_URL)


@post_required
def signup_register(request):
	pprint(request.POST)
	
	control = UserRegControl()
	if control.parseRequest(request.POST) == False:
		return __redirect(request, settings.INVALID_REQUEST_URL)

	error = None
	if control.validate():
		user = control.register()
		if user != None:
			print('registration successful')
			backends.login(request, user)
			return __redirect(request, settings.USER_SIGNUP_SUCCESS_URL)
		else:
			error = {'user':'server error, try again later'}

	if error == None:
		error = control.get_errors()

	if request.is_ajax():
		return JsonResponse({'status':401, 'message': 'Something wrong', 'error':error})
	else:
		request.session['form_values'] = control.get_values()
		request.session['form_errors'] = error
		return __redirect(request, settings.USER_SIGNUP_URL)


@login_required
def signup_success_view(request):
	print('registration success')
	data = {'title':'Signup :: Success', 'page':'user'}
	file = device.get_template(request, 'user_registered.html');
	return render(request, file, data)


@login_required
def profile_view(request):
	print('profile')
	user = User.get_user(request.user)
	dataurl = 'data-url="'+settings.USER_PROFILE_URL+'"'
	data = {'title':'Profile', 'page':'user', 'dataurl':dataurl, 'user': user}
	file = device.get_template(request, 'user_profile.html');
	return render(request, file, data)


## User personal and profile info
##

def user_info_view(request):
	return profile_view(request);


@login_required
def user_topics_select_view(request):
	data = {'title': 'Follow Topics', 'page':'user'};
	topics = Topic.get_topics(request.user)
	data.update({'topics':topics})
	file = device.get_template(request, 'user_topics_select.html')
	return render(request, file, data)


@login_required
def user_topic_selected(request):
	pprint(request.POST)
	error = None
	msg = None
	topic_id = request.POST.get('topic_id', -1)
	topic_followed = int(request.POST.get('topic_followed', 0))
	if topic_followed == 0:
		if TopicFollower.add_follower(request.user, topic_id):
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
			return JsonResponse({'status':204, 'message': msg})
		else:
			return JsonResponse({'status':401, 'error': error})
	else:
		return __redirect(request, settings.HOME_PAGE_URL)


def user_mails_view(request):
	data = {'title': 'User mails', 'page':'user'};
	file = device.get_template(request, 'user_mails.html')
	return render(request, file, data)


def user_stats_view(request):
	data = {'title': 'User stats', 'page':'user'};
	file = device.get_template(request, 'user_stats.html')
	return render(request, file, data)


def user_settings_view(request):
	data = {'title': 'User settings', 'page':'user'};
	file = device.get_template(request, 'user_settings.html')
	return render(request, file, data)