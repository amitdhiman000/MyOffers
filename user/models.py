import hashlib
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
#from time import timezone
from datetime import datetime
from locus.models import Area
from apputil import App_UserFilesDir

## debug
import traceback
from pprint import pprint


class User(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False, default='')
	email = models.EmailField()
	password = models.CharField(max_length=32, blank=False, default='')
	created_at = models.DateTimeField(default=timezone.now)
	phone = models.CharField(max_length=10, blank=True)
	# {-2: delete, -1:blocked, 0:inactive, 1:active }
	status = models.IntegerField(default=1)
	# {0:guest, 1:normal, 2:morderator, 3:author, 9:admin}
	level = models.IntegerField(default=1)
	image = models.FileField(upload_to=App_UserFilesDir, default=settings.DEFAULT_USER_IMAGE)

	@classmethod
	def create(klass, user):
		try:
			return klass.objects.create(name=user.name,
					email=user.email,
					password=user.password,
					phone=user.phone,
					level=9)
		except:
			print('failed to create user')
			traceback.print_exc()
			return None

	@classmethod
	def get_user(klass, user):
		try:
			return klass.objects.get(email=user.email)
		except:
			print("failed to get user")
			traceback.print_exc()
			return None

	@classmethod
	def get_user_by_id(klass, user_id):
		try:
			return klass.objects.get(id=user_id)
		except:
			print("failed to get user")
			traceback.print_exc()
			return None

	def get_absolute_url(self):
		return '/user/%s/' % urlquote(self.email)

	def get_name(self):
		return self.name
	##
	## Always return True, user object is created means loggedin.
	def is_loggedin(self):
		return True

	def email_user(self, from_email=None, subject='Hello', message=None):
		send_mail(subject, message, from_email, self.email)


class Guest:
	def __init__(self):
		#self.email = ''
		self.name = 'Guest'

	def get_full_name(self):
		return self.name

	def is_loggedin(self):
		return False

class Address(models.Model):
	id = models.BigAutoField(primary_key=True)
	line1 = models.CharField(max_length=50, blank=True)
	line2 = models.CharField(max_length=50, blank=True)
	geo_long = models.CharField(max_length=10, blank=True)
	geo_lat = models.CharField(max_length=10, blank=True)
	fk_area = models.ForeignKey(Area, on_delete=models.CASCADE)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
