from django.conf import settings
from django.db import models
from base.models import BaseModel
from datetime import (datetime, timedelta)
from django.utils import timezone
from django.utils.translation import ugettext as _

from user.models import User
from locus.models import Address
from business.models import Category
from business.models import Business
from base.apputil import App_UserFilesDir


# Create your models here.
def days_ahead(days=1):
	return timezone.now() + timezone.timedelta(days=days)


# offers table for new offers
class Offer(BaseModel):
	id = models.BigAutoField(primary_key=True)
	slug = models.SlugField(unique=True)
	name = models.CharField(max_length=30, blank=False)
	details = models.TextField()
	image = models.FileField(upload_to=App_UserFilesDir)
	price = models.IntegerField(default=100) ## MRP
	discount = models.IntegerField(default=0)
	discount_price = models.IntegerField(default=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	start_at = models.DateTimeField(default=timezone.now())
	expire_at = models.DateTimeField(default=days_ahead(5))
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)


	class Meta:
		verbose_name = _('offer')
		verbose_name_plural= _('offers')


	def __str__(self):
		return self.name


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
