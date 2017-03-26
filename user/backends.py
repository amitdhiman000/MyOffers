from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.conf import settings
from .models import User, Guest

USER_UID_KEY = '_user_uid'
USER_EMAIL_KEY = '_user_name'
USER_NAME_KEY = '_user_email'
USER_LEVEL_KEY = '_user_level'
USER_AUTH_KEY = '_user_auth'


def get_user(request):
	user = None
	if USER_EMAIL_KEY in request.session:
		uid = request.session[USER_UID_KEY]
		email = request.session[USER_EMAIL_KEY]
		name = request.session[USER_NAME_KEY]
		level = request.session[USER_LEVEL_KEY]
		user = User(id=uid, email=email, name=name, level=level)
	else:
		user = Guest()

	#print ('user name : '+user.name)
	return user


def auth_user(email, password):
	user = None
	try:
		user = User.objects.get(email=email, password=password)
	except ObjectDoesNotExist:
		user = None
	return user


def login(request, user):
	# need to do it in accounts.middleware.AuthMiddleware
	request.session[USER_UID_KEY] = user.id
	request.session[USER_EMAIL_KEY] = user.email
	request.session[USER_NAME_KEY] = user.name
	request.session[USER_LEVEL_KEY] = user.level
	request.session[USER_AUTH_KEY] = True
	request.session.set_expiry(60*60) # 10 minutes session timeout


def logout(request):
	request.session.flush()
	request.user = Guest()
	#request._cached_user = request.user
