import os
import hashlib
from django.conf import settings

from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext as _
#from time import timezone
from datetime import datetime

## debug
import traceback
from pprint import pprint


class User(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False, default='')
	email = models.EmailField()
	password = models.CharField(max_length=32, blank=False, default='')
	created = models.DateTimeField(default=timezone.now)
	phone = models.CharField(max_length=10, blank=True)
	# {-2: delete, -1:blocked, 0:inactive, 1:active }
	status = models.IntegerField(default=1)
	# {0:guest, 1:normal, 2:morderator, 3:author, 9:admin}
	level = models.IntegerField(default=1)

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
			return klass.objects.get(pk=user_id)
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


class Country(models.Model):
	country_id = models.IntegerField(primary_key=True, unique=True, null=False)
	country_name = models.CharField(max_length=50, blank=False)

	class Meta:
		verbose_name = _('country')
		verbose_name_plural= _('countries')

	@classmethod
	def add(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		obj = klass.objects.get_or_create(country_name=name)[0]
		return (obj != None)

	@classmethod
	def remove(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(country_name=name)[0]
			return True
		except:
			traceback.print_exc()
			return False

	@classmethod
	def get(klass, name):
		try:
			return klass.objects.get(country_name=name)
		except:
			print('Failed to get country')
			traceback.print_exc()
			return None

	@classmethod
	def get_all(klass):
		objs = klass.objects.all()
		return objs;

class State(models.Model):
	state_id = models.IntegerField(primary_key=True, unique=True, null=False)
	state_name = models.CharField(max_length=50, blank=True)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('state')
		verbose_name_plural= _('states')

	@classmethod
	def add(klass, state_name, country_name = 'India'):
		if state_name == None or state_name == '':
			raise ValueError('Invalid value')
		try:
			country = Country.objects.get(country_name=country_name)
			obj = klass.objects.get_or_create(state_name=state_name, fk_country=country)[0]
			return obj
		except:
			print('Failed to get country'+ country_name)
			traceback.print_exc()
			return False

	@classmethod
	def remove(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(state_name=name)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False

	@classmethod
	def get_all(klass, country_name):
		try:
			country = Country.objects.get(country_name=country_name)
			objs = klass.objects.filter(fk_country=country)
			return objs
		except:
			print("Failed to get country")
			traceback.print_exc()
			return None

class City(models.Model):
	city_id = models.IntegerField(primary_key=True, unique=True)
	city_name = models.CharField(max_length=50)
	fk_state = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('city')
		verbose_name_plural= _('cities')

	@classmethod
	def add(klass, city_name, country_name='India', state_name='Karnataka'):
		if city_name == None or city_name == '':
			raise ValueError('Invalid value')

		try:
			country = Country.objects.get(country_name=country_name)
			state = State.objects.get(state_name=state_name)
			obj = klass.objects.get_or_create(city_name=city_name, fk_state=state, fk_country=country,)[0]
			return obj
		except:
			print('Failed to add city')
			traceback.print_exc()
			return None

	@classmethod
	def remove(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(city_name=name)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False


class Area(models.Model):
	area_id = models.IntegerField(primary_key=True, unique=True, null=False)
	area_name = models.CharField(max_length=50, blank=True)
	area_pin = models.CharField(max_length=10, blank=True)
	fk_city = models.ForeignKey(City, on_delete=models.CASCADE)
	fk_state = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('area')
		verbose_name_plural= _('areas')


	@classmethod
	def add(klass, area_name, area_pin, country_name, state_name, city_name):
		if area_name == None or area_name == '':
			raise ValueError('Invalid value')
		try:	
			country = Country.objects.get(country_name=country_name)
			state = State.objects.get(state_name=state_name)
			city = City.objects.get(city_name=city_name)
			obj = klass.objects.get_or_create(area_name=area_name, area_pin=area_pin, fk_country=country, fk_state=state, fk_city=city)[0]
			return (obj != None)
		except:
			traceback.print_exc()
			return None

	@classmethod
	def remove(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(area_name=name)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False

	@classmethod
	def get(klass, area_name, area_pin):
		try:
			return klass.objects.filter(area_pin=area_pin)[0]
		except:
			traceback.print_exc()
			return None

	@classmethod
	def get_match(klass, keyw):
		print('key is : '+keyw)
		query = klass.objects.annotate(city=models.F('fk_city__city_name'), name=models.F('area_name'), pin=models.F('area_pin')).filter(area_name__istartswith=keyw).values('name', 'pin', 'city')[:20]
		#query = klass.objects.annotate(city_name=models.F('fk_city__city_name')).filter(area_name__icontains=keyw).values('area_name', 'area_pin', 'city_name')
		return query


class Address(models.Model):
	address_id = models.IntegerField(primary_key=True, unique=True)
	house_info = models.CharField(max_length=50, blank=True)
	geo_long = models.CharField(max_length=10, blank=True)
	geo_lat = models.CharField(max_length=10, blank=True)
	fk_area = models.ForeignKey(Area, on_delete=models.CASCADE)


def user_files_dir(inst, filename):
	# file will be uploaded to MEDIA_ROOT/products/user_<id>/<filename>
	path = os.path.join(settings.MEDIA_USER_FILES_DIR_NAME, 'user_{0}/{1}_{2}'.format(inst.fk_user.id, timezone.now(), filename))
	print(path)
	return path

class FileUpload(models.Model):
	id = models.BigAutoField(primary_key=True)
	file = models.FileField(upload_to=user_files_dir)
	used = models.IntegerField(default=0)
	created = models.DateTimeField(default=timezone.now)
	fk_user = models.ForeignKey(User)

	@classmethod
	def create(klass, file_data, user):
		obj = klass(file=file_data, fk_user=user)
		obj.save()
		return obj

	@classmethod
	def remove(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			if obj.used == 0:
				# delete the file from disk
				obj.file.delete()
			obj.delete()
			return True
		except:
			print('Failed to delete file')
			traceback.print_exc()
			return False

	@classmethod
	def get_file(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			return obj
		except:
			print('Failed to get file name')
			traceback.print_exc()
			return None

	@classmethod
	def mark_used(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			obj.used = 1
			obj.save()
			return True
		except:
			print('Failed to mark as used')
			traceback.print_exc()
			return False
