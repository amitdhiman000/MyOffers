from django.conf import settings
from django.db import models
from django.utils.translation import ugettext as _

## debug
import traceback
from pprint import pprint

class Country(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False)

	class Meta:
		verbose_name = _('country')
		verbose_name_plural= _('countries')


	@classmethod
	def add_country(klass, country_name):
		if country_name == None or country_name == '':
			raise ValueError('Invalid value')
		obj = klass.objects.get_or_create(name=country_name)[0]
		return obj


	@classmethod
	def add(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		return klass.objects.get_or_create(name=name)[0]


	@classmethod
	def remove(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(name=name)[0]
			return True
		except:
			traceback.print_exc()
			return False


	@classmethod
	def get(klass, name):
		try:
			return klass.objects.get(name=name)
		except:
			print('Failed to get country')
			traceback.print_exc()
			return None


	@classmethod
	def get_all(klass):
		objs = klass.objects.all()
		return objs;




class State(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('state')
		verbose_name_plural= _('states')


	@classmethod
	def add_state(klass, state_name, country):
		if state_name == None or state_name == '':
			raise ValueError('Invalid value')
		obj = klass.objects.get_or_create(name=state_name, fk_country=country)[0]
		return obj


	@classmethod
	def add(klass, state_name, country_name = 'India'):
		if state_name == None or state_name == '':
			raise ValueError('Invalid value')
		try:
			country = Country.objects.get(country_name=country_name)
			obj = klass.objects.get_or_create(name=state_name, fk_country=country)[0]
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
			obj = klass.objects.get(name=name)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False


	@classmethod
	def get_all(klass, country_name):
		try:
			country = Country.objects.get(name=country_name)
			objs = klass.objects.filter(fk_country=country)
			return objs
		except:
			print("Failed to get states")
			traceback.print_exc()
			return None




class City(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50)
	fk_state = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('city')
		verbose_name_plural= _('cities')


	@classmethod
	def add_city(klass, city_name, state, country):
		if city_name == None or city_name == '':
			raise ValueError('Invalid value')
		obj = klass.objects.get_or_create(name=city_name, fk_state=state, fk_country=country)[0]
		return obj


	@classmethod
	def add(klass, city_name, country_name='India', state_name='Karnataka'):
		if city_name == None or city_name == '':
			raise ValueError('Invalid value')
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			obj = klass.objects.get_or_create(name=city_name, fk_state=state, fk_country=country,)[0]
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
			obj = klass.objects.get(name=name)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False


	@classmethod
	def get_all(klass, country_name, state_name):
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			objs = klass.objects.filter(fk_country=country, fk_state=state)
			return objs
		except:
			print("Failed to get cites")
			traceback.print_exc()
			return None


	@classmethod
	def get_by_name(klass, name):
		try:
			return klass.objects.get(name=name)
		except:
			traceback.print_exc()
			return None




class Area(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True)
	pin = models.CharField(max_length=10, blank=True)
	fk_city = models.ForeignKey(City, on_delete=models.CASCADE)
	fk_state = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('area')
		verbose_name_plural= _('areas')


	@classmethod
	def add_area(klass, area_name, area_pin, city, state, country):
		if area_name == None or area_name == '' or area_pin == None or area_pin == '':
			raise ValueError('Invalid value')
		obj = klass.objects.get_or_create(name=area_name, pin=area_pin, fk_city=city, fk_state=state, fk_country=country)[0]
		return obj


	@classmethod
	def add(klass, area_name, area_pin, city_name, state_name, country_name):
		if area_name == None or area_name == '':
			raise ValueError('Invalid value')
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			city = City.objects.get(name=city_name)
			obj = klass.objects.get_or_create(name=area_name, pin=area_pin, fk_country=country, fk_state=state, fk_city=city)[0]
			return (obj != None)
		except:
			traceback.print_exc()
			return None


	@classmethod
	def remove(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(name=name)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False


	@classmethod
	def get_all(klass, country_name, state_name, city_name):
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			city = City.objects.get(name=city_name)
			objs = klass.objects.filter(fk_country=country, fk_state=state, fk_city=city)
			return objs
		except:
			print("Failed to get areas")
			traceback.print_exc()
			return None


	@classmethod
	def get_area(klass, country_name, state_name, city_name, area_name):
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			city = City.objects.get(name=city_name)
			objs = klass.objects.filter(name=area_name, fk_country=country, fk_state=state, fk_city=city)
			return objs
		except:
			print("Failed to get area")
			traceback.print_exc()
			return None


	@classmethod
	def get_by_pin(klass, area_name, area_pin):
		try:
			return klass.objects.filter(pin=area_pin)[0]
		except:
			traceback.print_exc()
			return None


	@classmethod
	def get_by_city(klass, city):
		try:
			return klass.objects.filter(fk_city__name=city)
		except:
			print('Failed to get areas')
			traceback.print_exc()
			return None


	@classmethod
	def get_by_match(klass, keyw):
		print('key is : '+keyw)
		query = klass.objects.annotate(city=models.F('fk_city__name')).filter(name__istartswith=keyw).values('name', 'pin', 'city')[:20]
		#query = klass.objects.annotate(city_name=models.F('fk_city__city_name')).filter(area_name__icontains=keyw).values('area_name', 'area_pin', 'city_name')
		return query

'''
class Location(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False)
	landmark = models.CharField(max_length=50, blank=True)
	logitude = models.CharField(max_length=10, blank=True)
	latitude = models.CharField(max_length=10, blank=True)
	fk_area = models.ForeignKey(Area, on_delete=models.CASCADE)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

	@classmethod
	def add(klass, loc_name, landmark, logitude, latitude, user, area):
		if loc_name == None or loc_name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get_or_create(name=loc_name, landmark=landmark, longitude=longitude, latitude=latitude, fk_area=area)[0]
			return obj
		except:
			print('Failed to add location')
			traceback.print_exc()
			return None


	@classmethod
	def remove(klass, name, user):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(name=name)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False
'''