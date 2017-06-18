from django.conf import settings
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from user_agents import parse


## decorator function check for request method, if not GET redirect to invalid reguest page.
##
def get_required(funct):
	def _decorator(request, *args, **kwargs):
		if request.method != 'GET':
			return __redirect(request, settings.ERROR_INVALID_REQUEST_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## decorator function check for request method, if not POST redirect to invalid reguest page.
##
def post_required(funct):
	def _decorator(request, *args, **kwargs):
		if request.method != 'POST':
			return __redirect(request, settings.ERROR_INVALID_REQUEST_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## Decorator function for chekcing the login status and redirect to login page
##
def login_required(funct):
	#@warps(funct)
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == False:
			return __redirect(request, settings.USER_LOGIN_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## Decorator function for checking the login user is admin or not
##
def admin_required(funct):
	#@warps(funct)
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == False:
			return __redirect(request, settings.USER_LOGIN_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		elif request.user.level != settings.ADMIN_LEVEL:
			return __redirect(request, settings.ERROR_ACCESS_DENIED_URL)
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## Decorator function for chekcing the login status and redirect to home page
##
def redirect_if_loggedin(funct):
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == True:
			return __redirect(request, settings.USER_PROFILE_URL)
		return funct(request, *args, **kwargs)
	return _decorator


## class for mocking any object
##
class Klass:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)


## helper functions common to all views
##

def __render(request, param, file, data):
	file_path = get_template(request, file, param)
	return render(request, file_path, data)


def __redirect(request, url):
	if request.is_ajax():
		return JsonResponse({'status':302, 'url': url})
	return HttpResponseRedirect(url)


def __template(request, file):
	page_id  = request.GET.get('pid', '')
	if request.is_ajax() == False or page_id < '2' or page_id > '3':
		page_id = ''

	ua_string = request.META.get('HTTP_USER_AGENT', '').lower()
	user_agent = parse(ua_string)
	base = 'responsive/'
	if user_agent.is_mobile:
		base = 'mobile/'
	else:
		base = 'desktop/'

	file_path = base+file[:-5]+page_id+'.html'
	print(file_path)
	return file_path
