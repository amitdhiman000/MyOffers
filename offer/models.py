import os
from django.conf import settings
from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import ugettext as _

from locus.models import Address
from user.models import User

from common.apputil import App_UserFilesDir

## debug
import traceback
from pprint import pprint

# Create your models here.
def days_ahead(days=1):
	return timezone.now() + timezone.timedelta(days=days)



# Business types
class Category(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=30)
	details = models.CharField(max_length=50)
	parent = models.ForeignKey("self", default=None, null=True, blank=True)

	class Meta:
		verbose_name = _('category')
		verbose_name_plural= _('categories')

	def __str__(self):
		return self.name


	@classmethod
	def create(klass, parent, name, desc):
		return klass.objects.create(parent=parent, name=name, details=desc)


	@classmethod
	def remove(klass, name):
		try:
			db_obj = klass.objects.get(name=name)
			db_obj.delete()
			return True
		except:
			print('failed to delete')
			traceback.print_exc()
			return False


	@classmethod
	def fetch_all(klass):
		return klass.objects.all()


	@classmethod
	def fetch_by_id(klass, id):
		try:
			return klass.objects.get(id=id)
		except:
			traceback.print_exc()
			return None


	@classmethod
	def fetch_by_name(klass, name):
		try:
			return klass.objects.get(name=name)
		except:
			traceback.print_exc()
			return None


	@classmethod
	def fetch_children(klass, name):
		return klass.objects.filter(parent__name=name)



# Business
class Business(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False)
	desc = models.CharField(max_length=100, blank=False)
	website = models.CharField(max_length=100, blank=True)
	fk_category = models.ForeignKey(Category)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
	#fk_address = models.ForeignKey(Address)


	@classmethod
	def create(klass, b, user):
		obj = klass.objects.get_or_create(name=b.name, desc=b.desc, website=b.website, fk_category=b.category, fk_user=user)[0]
		return obj


	@classmethod
	def remove(klass, id, name, user):
		if name == None or name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get(id=id, name=name, fk_user=user)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False


	@classmethod
	def fetch_by_user(klass, user):
		return klass.objects.filter(fk_user=user)



class BusinessAdressMap(models.Model):
	id = models.BigAutoField(primary_key=True)
	fk_business = models.ForeignKey(Business, on_delete=models.CASCADE)
	fk_address = models.ForeignKey(Address, on_delete=models.CASCADE)

	@classmethod
	def create(klass, business, address):
		return klass.objects.get_or_create(fk_business=business, fk_address=address)


	@classmethod
	def remove(klass, business, address):
		try:
			db_obj = klass.objects.get(business, address)
			db_obj.delete()
			return True
		except:
			print('failed to delete')
			traceback.print_exc()
			return False


	@classmethod
	def fetch_by_business(klass, business):
		db_objs = klass.objects.filter(fk_business=business)
		return db_objs



# offers table for new offers
class Offer(models.Model):
	id = models.BigAutoField(primary_key=True)
	slug = models.SlugField(unique=True)
	name = models.CharField(max_length=30, blank=False)
	details = models.TextField()
	image = models.FileField(upload_to=App_UserFilesDir)
	price = models.IntegerField(default=100) ## MRP
	discount = models.IntegerField(default=0)
	discount_price = models.IntegerField(default=100)
	created_at = models.DateTimeField(default=timezone.now)
	start_at = models.DateTimeField(default=timezone.now)
	expire_at = models.DateTimeField(default=days_ahead(5))
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)


	class Meta:
		verbose_name = _('offer')
		verbose_name_plural= _('offers')


	def __str__(self):
		return self.name


	@classmethod
	def create(klass, obj):
		obj.save()
		return obj


	@classmethod
	def remove(klass, obj):
		try:
			db_obj = klass.objects.get(obj)
			db_obj.delete()
			return True
		except:
			print('failed to delete')
			traceback.print_exc()
			return False


	@classmethod
	def create_url_to_dict(klass, db_objs):
		for db_obj in db_objs:
			db_obj['url'] = '/offer/'+db_obj['slug']
		return db_objs


	@classmethod
	def create_url_to_objs(klass, db_objs):
		for db_obj in db_objs:
			db_obj.url = '/offer/'+db_obj.slug
		return db_objs


	@classmethod
	def create_url_to_obj(klass, db_obj):
		if db_obj:
			db_obj.url = '/offer/'+db_obj.slug
		return db_obj


	@classmethod
	def fetch_all(klass):
		db_objs = klass.objects.all()
		return klass.create_url_to_objs(db_objs)


	@classmethod
	def fetch_by_id(klass, id):
		try:
			db_objs = klass.objects.get(id=id)
			return klass.create_url_to_objs(db_objs)
		except:
			print('Failed to get product')
			traceback.print_exc()
			return None


	@classmethod
	def fetch_by_slug(klass, slug):
		try:
			db_obj = klass.objects.get(slug=slug)
			return klass.create_url_to_obj(db_obj)
		except:
			print('Failed to get product')
			traceback.print_exc()
			return None


	@classmethod
	def fetch_by_match(klass, keyw):
		try:
			db_objs = klass.objects.filter(name__contains=keyw).values('id', 'name', 'slug')[:10]
			return klass.create_url_to_dict(db_objs)
		except:
			traceback.print_exc()
			return []




class OfferCategoryMap(models.Model):
	id = models.BigAutoField(primary_key=True)
	fk_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
	fk_category = models.ForeignKey(Category, db_index=True, on_delete=models.CASCADE)

	@classmethod
	def create(klass, offer, category):
		obj = klass.create(fk_offer=offer, fk_category=category)
		return obj

	@classmethod
	def remove(klass, offer):
		try:
			db_obj = klass.objects.get(fk_offer=offer)
			db_obj.delete()
			return True
		except:
			print('failed to delete')
			traceback.print_exc()
			return False




class OfferLocationMap(models.Model):
	id = models.BigAutoField(primary_key=True)
	fk_offer = models.ForeignKey(Offer, on_delete=models.CASCADE)
#	fk_location = models.ForeignKey(Location, db_index=True, on_delete=models.CASCADE)
	fk_address = models.ForeignKey(Address, db_index=True, on_delete=models.CASCADE)

	@classmethod
	def create(klass, offer, loc):
		obj = klass.create(fk_offer=offer, fk_location=loc)
		return obj

	@classmethod
	def remove(klass, offer):
		try:
			db_obj = klass.objects.get(obj)
			db_obj.delete()
			return True
		except:
			print('failed to delete')
			traceback.print_exc()
			return False
