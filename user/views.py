from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.template.context_processors import csrf
from django.views.decorators.csrf import csrf_exempt

## custom packages
from apputil import *
from apputil import App_Redirect
from apputil import App_Render
## custom authentication
from . import backends
from user.models import User
from locus.models import Address
from user.control import UserRegControl
from user.control import UserSignInControl

## debugging
from pprint import pprint
# Create your views here.

@App_RedirectIfLoggedin
def signin_view(request):
	data = {'title':'Login', 'page':'user'}
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
	data = {'title':'Signup', 'page':'user'}
	data.update(csrf(request))
	data.update({settings.USER_LOGIN_NEXT: request.POST.get(settings.USER_LOGIN_NEXT, '')})
	if 'form_errors' in request.session:
		data['form_errors'] = request.session['form_errors']
		data['form_values'] = request.session['form_values']
		del request.session['form_errors']
		del request.session['form_values']

	return App_Render(request, 'user/user_signup_1.html', data)



def signout(request):
	backends.logout(request)
	return App_Redirect(request, settings.USER_LOGIN_URL)



@App_RedirectIfLoggedin
@App_PostRequired
def signin_auth(request):
	pprint(request.POST)
	error = None
	redirect_url = None

	control = UserSignInControl()
	if control.parseRequest(request.POST) and control.signin(request):
		redirect_url = request.POST.get(settings.USER_LOGIN_NEXT, '')
		if '' == redirect_url:
			redirect_url = settings.HOME_URL
		print('redirect amit : '+redirect_url)
		return App_Redirect(request, redirect_url)

	## Only error case will reach here.
	if request.is_ajax():
		error = control.errors()
		return JsonResponse({'status':401, 'error':error})
	else:
		redirect_url = request.META.get('HTTP_REFERER', settings.USER_LOGIN_URL)
		request.session['form_errors'] = control.errors()
		request.session['form_values'] = control.values()
		return App_Redirect(request, redirect_url)



@App_PostRequired
def signup_register(request):
	pprint(request.POST)

	control = UserRegControl()
	if control.parseRequest(request.POST) == False:
		return App_Redirect(request, settings.INVALID_REQUEST_URL)

	error = None
	if control.validate():
		user = control.register()
		if user != None:
			print('registration successful')
			backends.login(request, user)
			return App_Redirect(request, settings.USER_SIGNUP_SUCCESS_URL)
		else:
			error = {'user':'server error, try again later'}

	if error == None:
		error = control.errors()

	if request.is_ajax():
		return JsonResponse({'status':401, 'message': 'Something wrong', 'error':error})
	else:
		request.session['form_errors'] = error
		request.session['form_values'] = control.values()
		return App_Redirect(request, settings.USER_SIGNUP_URL)



@App_LoginRequired
def signup_success_view(request):
	print('registration success')
	data = {'title':'Signup | Success', 'page':'user'}
	return App_Render(request, 'user/user_registered_1.html', data)



@App_LoginRequired
def profile_view(request):
	user = User.fetch_user(request.user)
	address = Address.fetch_by_user(user)
	user.address = address
	data = {'title':'Profile', 'page':'user', 'user': user}
	return App_Render(request, 'user/user_profile_1.html', data)



## User personal and profile info
##
def user_info_view(request):
	return profile_view(request);



@App_LoginRequired
def user_topics_view(request):
	data = {'title': 'Follow Topics', 'page':'user'};
	topics = {}#Topic.fetch_topics(request.user)
	data.update({'topics':topics})
	return App_Render(request, 'user/user_topics_1.html', data)



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
			return JsonResponse({'status':204, 'message': msg})
		else:
			return JsonResponse({'status':401, 'error': error})
	else:
		return App_Redirect(request, settings.HOME_PAGE_URL)



@App_LoginRequired
def user_mails_view(request):
	print(request.GET.urlencode())
	data = {'title': 'User mails', 'page':'user'}
	return App_Render(request, 'user/user_mails_1.html', data)



@App_LoginRequired
def user_stats_view(request):
	data = {'title': 'User stats', 'page':'user'};
	return App_Render(request, 'user/user_stats_1.html', data)


@App_LoginRequired
def user_wishlist_view(request):
	data = {'title': 'User Wishlist', 'page':'user'};
	return App_Render(request, 'user/user_wishlist_1.html', data)


@App_LoginRequired
def user_settings_view(request):
	data = {'title': 'User settings', 'page':'user'};
	return App_Render(request, 'user/user_settings_1.html', data)
