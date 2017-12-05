import os
from django.utils import timezone
from django.conf import settings
from django.shortcuts import render
from django.http import (HttpResponseRedirect,
HttpResponse, JsonResponse)
from user_agents import parse
from datetime import (datetime, timedelta)



## JSON Web Token
##
import jwt
def App_CreateToken(request, user):
	if user == None:
		return None
	payload = { 'user_id':user.id, 'exp': datetime.utcnow() + timedelta(seconds=600)}
	token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
	return token.decode('utf-8')


def App_RefreshToken(request, user):
	if user == None:
		return None
	if App_VerifyToken(request):
		return App_CreateToken(request, user)
	return None


def App_VerifyToken(request):
	token = request.META.get('HTTP_AUTHORIZATION', 'a:b')
	print('auth token : '+ token)
	try:
		payload = jwt.decode(token, settings.SECRET_KEY, algorithm='HS256')
		uid = payload['user_id']
		#request.user = Klass(id=uid)
		return True
	except Exception as e:
		print(e)
	return False


def App_TokenRequired(funct):
	def _decorator(self, request, *args, **kwargs):
		if App_VerifyToken(request) == False:
			return JsonResponse({'result': {'message': 'Token expired'}}, status=401)
		else:
			return funct(self, request, *args, **kwargs)
	return _decorator;


## decorator function check for request method, if not GET redirect to invalid reguest page.
##
def App_GetRequired(funct):
	def _decorator(request, *args, **kwargs):
		if request.method != 'GET':
			return App_Redirect(request, settings.ERROR_INVALID_REQUEST_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## decorator function check for request method, if not POST redirect to invalid reguest page.
##
def App_PostRequired(funct):
	def _decorator(request, *args, **kwargs):
		if request.method != 'POST':
			return App_Redirect(request, settings.ERROR_INVALID_REQUEST_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## Decorator function for chekcing the login status and redirect to login page
##
def App_LoginRequired(funct):
	#@warps(funct)
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == False:
			redirect_url = settings.USER_LOGIN_URL + "?"+settings.USER_LOGIN_NEXT+"="+request.path
			return App_Redirect(request, redirect_url)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## Decorator function for checking the login user is admin or not
##
def App_AdminRequired(funct):
	#@warps(funct)
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == False:
			return App_Redirect(request, settings.USER_LOGIN_URL)
			#if 'application/json' in request.META.get('HTTP_ACCEPT'):
		elif request.user.level != settings.ADMIN_LEVEL:
			return App_Redirect(request, settings.ERROR_ACCESS_DENIED_URL)
		else:
			return funct(request, *args, **kwargs)
	return _decorator;


## Decorator function for chekcing the login status and redirect to home page
##
def App_RedirectIfLoggedin(funct):
	def _decorator(request, *args, **kwargs):
		if request.user.is_loggedin() == True:
			return App_Redirect(request, settings.USER_PROFILE_URL)
		return funct(request, *args, **kwargs)
	return _decorator


def App_Time(funct):
	def _decorator(*args, **kwargs):
		t1 = time.time()
		retv = funct(request, *args, **kwargs)
		t2 = time.time() - t1
		print('{} ran in {} sec'.format(funct.__name__, t2))
		return retv
	return _decorator


## class for mocking any object
##
class Klass:
	def __init__(self, **kwargs):
		self.__dict__.update(kwargs)


def App_UserFilesDir(inst, filename):
	# file will be uploaded to MEDIA_ROOT/products/user_<id>/<filename>
	path = os.path.join(settings.MEDIA_USER_FILES_DIR_NAME, 'user_{0}/{1}_{2}'.format(inst.fk_user.id, timezone.now(), filename))
	print(path)
	return path


def App_Slugify(text):
	import re
	#text = unidecode.unidecode(text).lower()
	return re.sub(r'\W+', '-', text)


## helper functions common to all views
##
def App_Template(request, file):
	page_id  = request.GET.get('pid', '1')
	ua_string = request.META.get('HTTP_USER_AGENT', '')
	user_agent = parse(ua_string)
	'''
	print(ua_string)
	print(user_agent)
	print(user_agent.is_pc)
	print(user_agent.is_mobile)
	print(user_agent.is_tablet)
	print(user_agent.is_touch_capable)
	print(user_agent.is_bot)
	'''
	base_dir = 'responsive/'
	if user_agent.is_mobile:
		base_dir = 'mobile/'
	else:
		base_dir = 'desktop/'

	base_tpl = None
	if request.is_ajax():
		base_tpl = base_dir + settings.BASE_AJAX_TEMPLATE
	else:
		base_tpl = base_dir + settings.BASE_TEMPLATE

	file_path = base_dir + file[:-6] + page_id + '.html'
	print(base_tpl, file_path , page_id)
	return (base_tpl, file_path)


def App_Redirect(request, url):
	if request.is_ajax():
		return JsonResponse({'status':302, 'url': url})
	return HttpResponseRedirect(url)


def App_Render(request, file, data):
	base_tpl,file = App_Template(request, file)
	data.update({'base_template':base_tpl})
	return render(request, file, data)
