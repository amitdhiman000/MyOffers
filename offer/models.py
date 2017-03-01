from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext as _

# Create your models here.

class Country(models.Model):
	country_id = models.IntegerField(primary_key=True, unique=True, null=False)
	country_name = models.CharField(max_length=50, blank=True)

	class Meta:
		verbose_name = _('country')
		verbose_name_plural= _('countries')


class State(models.Model):
	state_id = models.IntegerField(primary_key=True, unique=True, null=False)
	state_name = models.CharField(max_length=50, blank=True)
	fk_country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('state')
		verbose_name_plural= _('states')


class City(models.Model):
	city_id = models.IntegerField(primary_key=True, unique=True, null=False)
	city_name = models.CharField(max_length=50, blank=True)
	fk_state_id = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('city')
		verbose_name_plural= _('cities')


class Location(models.Model):
	location_id = models.IntegerField(primary_key=True, unique=True, null=False)
	location_name = models.CharField(max_length=50, blank=True)
	location_pin = models.CharField(max_length=10, blank=True)
	fk_city_id = models.ForeignKey(City, on_delete=models.CASCADE)
	fk_state_id = models.ForeignKey(State, on_delete=models.CASCADE)
	fk_country_id = models.ForeignKey(Country, on_delete=models.CASCADE)

	class Meta:
		verbose_name = _('location')
		verbose_name_plural= _('locations')


# Business types
class Business(models.Model):
	business_id = models.IntegerField(primary_key=True, unique=True, null=False)
	business_name = models.CharField(max_length=30)
	business_desc = models.CharField(max_length=50)

	class Meta:
		verbose_name = _('business')
		verbose_name_plural= _('business')

	def __str__(self):
		return self.business_name

	def add_category(self, name=None, desc=''):
		if name is None:
			raise ValueError("Category Name is required!!")
		obj = Category(business_name=name, business_desc=desc)
		obj.save()


# offers table for new offers
class Offer(models.Model):
	product_name = models.CharField(max_length=30, blank=True)
	image_name = models.CharField(max_length=50, blank=False)
	discount = models.CharField(max_length=3, blank=True)
	start_date = models.DateTimeField(blank=True)
	expire_date = models.DateTimeField(blank=True)
	create_time = models.DateTimeField(auto_now_add=True, auto_now=False)
	description = models.TextField()
	fk_location = models.ForeignKey(Location)

	class Meta:
		verbose_name = _('offer')
		verbose_name_plural= _('offers')

	def __str__(self):
		# __unicode__ on Python 2
		return self.product_name

	@classmethod
	def get_all(klass):
		return klass.objects.all()

	def get_by_location(self, location='bengaluru', count=20):
		pass

	def get_by_keyword(self, keyword='', count=20):
		pass

	@classmethod
	def register(klass, obj):
		obj.save()

	def delete(klass, obj):
		pass

