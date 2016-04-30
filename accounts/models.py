from __future__ import unicode_literals

from django.db import models
from time import timezone
from datetime import datetime
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
import hashlib


class BaseUser(models.Model):
	uid = models.IntegerField(primary_key=True, unique=True)
	name = models.CharField(max_length=50, blank=False, default='')
	#email should be usique, It is our unique key.
	email = models.CharField(max_length=50, unique=True, blank=False, default='')
	password = models.CharField(max_length=32, blank=False, default='')
	created = models.DateTimeField(auto_now_add=True, auto_now=False, blank=False, null=True)
	address = models.TextField(blank=True, default='')
	geolat = models.CharField(max_length=10, blank=True)
	geolong = models.CharField(max_length=10, blank=True)
	phone = models.CharField(max_length=10, blank=True)

	class Meta:
		# it will not create the table for abstact class.
		abstract = True
		verbose_name = _('user')
		verbose_name_plural= _('users')

	def get_absolute_url(self):
		return '/users/%s/' % urlquote(self.email)

	def get_full_name(self):
		return self.name
	##
	## Always return True, user object is created means loggedin.
	def is_loggedin(self):
		return True

	def email_user(self, from_email=None, subject='Hello', message=None):
		send_mail(subject, message, from_email, self.email)


# Consumer user class
class Consumer(BaseUser):
	dob = models.CharField(max_length = 50)

	class Meta:
		verbose_name = _('Consumer')
		verbose_name_plural= _('Consumers')

	def add_consumer(self):
		self.save()


# Vendor user class
class Vendor(BaseUser):
	#business = models.OneToOneField(Business)

	class Meta:
		verbose_name = _('vendor')
		verbose_name_plural= _('vendors')

	def add_vendor(self):
		self.save()


class AnonymousUser:

	def __init__(self):
		self.email = ''
		self.name = 'Guest'

	def get_full_name(self):
		return self.name

	def is_loggedin(self):
		return False




