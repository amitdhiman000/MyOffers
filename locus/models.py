from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.apps import apps

from user.models import User
## debug
import logging
import traceback
from pprint import pprint



class Country(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False)

	class Meta:
		verbose_name = _('country')
		verbose_name_plural= _('countries')


	@classmethod
	def create(klass, name):
		return klass.objects.get_or_create(name=name)[0]


	@classmethod
	def fetch_or_create(klass, name):
		return klass.create(name)


	@classmethod
	def remove(klass, name):
		try:
			obj = klass.objects.get(name=name)[0]
			return True
		except Exception as e:
			logging.error(e)
			return False


	@classmethod
	def fetch_all(klass):
		objs = klass.objects.all()
		return objs;


	@classmethod
	def fetch_by_name(klass, name):
		try:
			return klass.objects.get(name=name)
		except Exception as e:
			logging.error(e)
			return None

	@classmethod
	def fetch_by_filter(klass, values):
		try:
			return klass.objects.filter(**values)
		except Exception as e:
			logging.error(e)
			return None



class State(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('state')
		verbose_name_plural= _('states')


	@classmethod
	def create(klass, state_name, country):
		obj = klass.objects.get_or_create(name=state_name, fk_country=country)[0]
		return obj


	@classmethod
	def create0(klass, state_name, country_name = 'India'):
		try:
			country = Country.objects.get(country_name=country_name)
			obj = klass.objects.get_or_create(name=state_name, fk_country=country)[0]
			return obj
		except Exception as e:
			logging.error(e)
			return False


	@classmethod
	def fetch_or_create(klass, state_name, country):
		return klass.create(state_name=state_name, country=country)


	@classmethod
	def remove(klass, name):
		try:
			obj = klass.objects.get(name=name)[0]
			obj.delete()
			return True
		except Exception as e:
			logging.error(e)
			return False


	@classmethod
	def fetch_all(klass, country_name):
		try:
			country = Country.objects.get(name=country_name)
			objs = klass.objects.filter(fk_country=country)
			return objs
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch(klass, name):
		try:
			return klass.objects.get(name=name)
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch_by_objs(klass, name, country):
		try:
			return klass.objects.get(name=name, fk_country=country)
		except Exception as e:
			logging.error(e)
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
	def create(klass, city_name, state, country):
		obj = klass.objects.get_or_create(name=city_name, fk_state=state, fk_country=country)[0]
		return obj


	@classmethod
	def create0(klass, city_name, country_name='India', state_name='Karnataka'):
		if city_name == None or city_name == '':
			raise ValueError('Invalid value')
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			obj = klass.objects.get_or_create(name=city_name, fk_state=state, fk_country=country,)[0]
			return obj
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch_or_create(klass, city_name, state, country):
		return klass.create(city_name, state, country)


	@classmethod
	def remove(klass, name):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(name=name)[0]
			obj.delete()
			return True
		except Exception as e:
			logging.error(e)
			return False


	@classmethod
	def fetch_all(klass, state_name, country_name):
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			objs = klass.objects.filter(fk_country=country, fk_state=state)
			return objs
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch(klass, name):
		try:
			return klass.objects.get(name=name)
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch_by_name(klass, city_name, state_name, country_name):
		try:
			return klass.objects.get(name=city_name, fk_state__name=state_name, fk_country__name=country_name)
		except Exception as e:
			logging.error(e)
			return None



class Area(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=True)
	pincode = models.CharField(max_length=10, blank=True)
	fk_city = models.ForeignKey(City, on_delete=models.CASCADE)
	fk_state = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('area')
		verbose_name_plural= _('areas')


	@classmethod
	def create(klass, values):
		obj = klass.objects.get_or_create(**values)[0]
		return obj


	@classmethod
	def fetch_or_create(klass, area_name, area_pin, city, state, country):
		values = {
			'name':area_name,
			'pincode':area_pin,
			'fk_city':city,
			'fk_state':state,
			'fk_country':country
		}
		return klass.create(values)


	@classmethod
	def remove(klass, values):
		try:
			obj = klass.objects.filter(**values)
			obj.delete()
			return True
		except Exception as e:
			logging.error(e)
			return False


	@classmethod
	def fetch_all(klass, city_name, state_name, country_name):
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			city = City.objects.get(name=city_name)
			objs = klass.objects.filter(fk_country=country, fk_state=state, fk_city=city)
			return objs
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch_by_name(klass, area_name, city_name, state_name, country_name):
		try:
			country = Country.objects.get(name=country_name)
			state = State.objects.get(name=state_name)
			city = City.objects.get(name=city_name)
			objs = klass.objects.filter(name=area_name, fk_country=country, fk_state=state, fk_city=city)
			return objs
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch_by_pincode(klass, area_pin):
		try:
			return klass.objects.filter(pincode=area_pin)
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch_by_city(klass, city):
		try:
			return klass.objects.filter(fk_city__name=city)
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def fetch_by_match(klass, keyw):
		print('key is : '+keyw)
		query = klass.objects.annotate(city=models.F('fk_city__name')).filter(name__istartswith=keyw).values('name', 'pin', 'city')[:20]
		#query = klass.objects.annotate(city_name=models.F('fk_city__city_name')).filter(area_name__icontains=keyw).values('area_name', 'area_pin', 'city_name')
		return query



from common.models import BaseModel
class Address(BaseModel):
	name = models.CharField(max_length=50, blank=False)
	phone = models.CharField(max_length=10, blank=True)
	address = models.CharField(max_length=50, blank=False)
	landmark = models.CharField(max_length=50, blank=True)
	latitude = models.CharField(max_length=10, blank=True)
	longitude = models.CharField(max_length=10, blank=True)
	created_at = models.DateTimeField(default=timezone.now)
	updated_at = models.DateTimeField(default=timezone.now)
	fk_area = models.ForeignKey(Area, on_delete=models.CASCADE)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
	flags = models.CharField(max_length=10, default='')


	def absolute_url(self):
		return '/locus/address/'+ str(self.id) + '/'


	@classmethod
	def queryset(klass):
		fields = ('id', 'name', 'pincode', 'address', 'area', 'city', 'state', 'country')
		return klass.objects.annotate(
		pincode=models.F('fk_area__pincode'),
		area=models.F('fk_area__name'),
		city=models.F('fk_area__fk_city__name'),
		state=models.F('fk_area__fk_state__name'),
		country=models.F('fk_area__fk_country__name')).values(*fields)


	@classmethod
	def fetch_all(klass):
		return klass.queryset()


	@classmethod
	def fetch_by_id(klass, id_):
		return klass.queryset().filter(id=id_)


	@classmethod
	def fetch_by_user(klass, user):
		return klass.queryset().filter(fk_user=user)



class Location(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False)
	latitude = models.CharField(max_length=10)
	longitude = models.CharField(max_length=10)

	@classmethod
	def create(klass, values):
		try:
			obj = klass.objects.get_or_create(**values)[0]
			return obj
		except Exception as e:
			logging.error(e)
			return None


	@classmethod
	def remove(klass, **values):
		try:
			obj = klass.objects.filter(**values)
			obj.delete()
			return True
		except Exception as e:
			logging.error(e)
			return False


	@classmethod
	def fetch_by_geo(klass, latitude, longitude):
		obj = klass.objects.get_or_create(latitude=latitude, longitude=longitude)
		return obj


	@classmethod
	def fetch_by_user(klass, user):
		return klass.objects.filter(fk_user=user)
