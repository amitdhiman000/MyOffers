import os
from django.conf import settings
from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import ugettext as _
from user.models import Area
from user.models import User

## debug
import traceback
from pprint import pprint

# Create your models here.
def days_ahead(days=1):
	return timezone.now() + timezone.timedelta(days=days)



def App_UserFilesDir(inst, filename):
	# file will be uploaded to MEDIA_ROOT/products/user_<id>/<filename>
	path = os.path.join(settings.MEDIA_USER_FILES_DIR_NAME, 'user_{0}/{1}_{2}'.format(inst.fk_user.id, timezone.now(), filename))
	print(path)
	return path


class Location(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False)
	landmark = models.CharField(max_length=50, blank=True)
	logitude = models.CharField(max_length=10, blank=True)
	latitude = models.CharField(max_length=10, blank=True)
	fk_area = models.ForeignKey(Area, on_delete=models.CASCADE)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

	@classmethod
	def create(klass, loc_name, landmark, logitude, latitude, user, area):
		if loc_name == None or loc_name == '':
			raise ValueError('Invalid value')
		try:
			obj = klass.objects.get_or_create(name=loc_name, landmark=landmark, longitude=longitude, latitude=latitude, fk_user=user, fk_area=area)[0]
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
			obj = klass.objects.get(name=name, fk_user=user)[0]
			obj.delete()
			return True
		except:
			traceback.print_exc()
			return False


# Business types
class Business(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=30)
	details = models.CharField(max_length=50)

	class Meta:
		verbose_name = _('business')
		verbose_name_plural= _('business')

	def __str__(self):
		return self.name

	@classmethod
	def create(klass, name, desc):
		obj = klass(name=name, details=desc)
		obj.save()



# Business types
class Category(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=30)
	details = models.CharField(max_length=50)
	parent = models.ForeignKey("self", default=1)

	class Meta:
		verbose_name = _('category')
		verbose_name_plural= _('categories')

	def __str__(self):
		return self.name


	@classmethod
	def create(klass, name, desc):
		return klass.objects.create(name=name, details=desc)


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
	def get_all(klass):
		return klass.objects.get_all()


	@classmethod
	def get(klass, name):
		return klass.objects.filter(parent__name=name)



# offers table for new offers
class Offer(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=30, blank=False)
	image = models.FileField(upload_to=App_UserFilesDir)
	price = models.IntegerField(default=100) ## MRP
	discount = models.IntegerField(default=0)
	discount_price = models.IntegerField(default=100)
	created_at = models.DateTimeField(default=timezone.now)
	start_at = models.DateTimeField(default=timezone.now)
	expire_at = models.DateTimeField(default=days_ahead(5))
	slug = models.SlugField(unique=True)
	details = models.TextField()
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
	#fk_category = models.ForeignKey(Category)
	#fk_location = models.ForeignKey(Location)
	#fk_area = models.ForeignKey(Area)

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
	def add_url_to_dict(klass, db_objs):
		for db_obj in db_objs:
			db_obj['url'] = '/offer/'+db_obj['slug']
		return db_objs


	@classmethod
	def add_url_to_objs(klass, db_objs):
		for db_obj in db_objs:
			db_obj.url = '/offer/'+db_obj.slug
		return db_objs


	@classmethod
	def add_url_to_obj(klass, db_obj):
		if db_obj:
			db_obj.url = '/offer/'+db_obj.slug
		return db_obj


	@classmethod
	def get_all(klass):
		db_objs = klass.objects.all()
		return klass.add_url_to_objs(db_objs)


	@classmethod
	def get_by_id(klass, id):
		try:
			db_objs = klass.objects.get(id=id)
			return klass.add_url_to_objs(db_objs)
		except:
			print('Failed to get product')
			traceback.print_exc()
			return None


	@classmethod
	def get_by_slug(klass, slug):
		try:
			db_obj = klass.objects.get(slug=slug)
			return klass.add_url_to_obj(db_obj)
		except:
			print('Failed to get product')
			traceback.print_exc()
			return None


	@classmethod
	def get_match(klass, keyw):
		try:
			db_objs = klass.objects.filter(name__contains=keyw).values('id', 'name', 'slug')[:10]
			return klass.add_url_to_dict(db_objs)
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
	fk_location = models.ForeignKey(Location, db_index=True, on_delete=models.CASCADE)

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
