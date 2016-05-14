from .models import Consumer, Vendor, AnonymousUser

from django.core.exceptions import ObjectDoesNotExist

USER_UID_KEY = '_user_uid'
USER_NAME_KEY = '_user_name'
USER_TYPE_KEY = '_user_type'
USER_AUTH_KEY = '_user_auth'


def auth_vendor(username='', password=''):
	user = None
	try:
		user = Vendor.objects.get(email=username, password=password)
	except ObjectDoesNotExist:
		user = None

	return user


def auth_consumer(username='', password=''):
	user = None
	try:
		user = Consumer.objects.get(email=username, password=password)
	except ObjectDoesNotExist:
		user = None

	return user

def get_user(request):
	user = None
	if USER_TYPE_KEY in request.session:
		if request.session[USER_TYPE_KEY] == 'Consumer':
			user = Consumer(name=request.session[USER_NAME_KEY])
		elif request.session[USER_TYPE_KEY] == 'Vendor':
			user = Vendor(name=request.session[USER_NAME_KEY])
	else:
		user = AnonymousUser()

	#print ('user name : '+user.name)
	return user


def login(request, user):
	# need to do it in accounts.middleware.AuthMiddleware
	#request.user = user
	request.session[USER_UID_KEY] = user._meta.pk.value_to_string(user)
	request.session[USER_NAME_KEY] = user.name
	request.session[USER_TYPE_KEY] = type(user).__name__
	print('class name : '+  type(user).__name__)
	request.session[USER_AUTH_KEY] = True
	request.session.set_expiry(60*5) # 5 minutes session timeout


def logout(request):
	request.session.flush()
	request.user = AnonymousUser()
	#request._cached_user = request.user