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



def user_files_dir(inst, filename):
	# file will be uploaded to MEDIA_ROOT/products/user_<id>/<filename>
	path = os.path.join(settings.MEDIA_USER_FILES_DIR_NAME, 'user_{0}/{1}_{2}'.format(inst.fk_user.id, timezone.now(), filename))
	print(path)
	return path



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
class Catagory(models.Model):
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



# offers table for new offers
class Offer(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=30, blank=False)
	image = models.FileField(upload_to=user_files_dir)
	price = models.IntegerField(default=100) ## MRP
	discount = models.IntegerField(default=0)
	discount_price = models.IntegerField(default=100)
	created_at = models.DateTimeField(default=timezone.now)
	start_at = models.DateTimeField(default=timezone.now)
	expire_at = models.DateTimeField(default=days_ahead(5))
	slug = models.SlugField(unique=True)
	details = models.TextField()
	fk_user = models.ForeignKey(User)
	fk_area = models.ForeignKey(Area)

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


	def get_by_location(self, location, count=20):
		pass

	def get_by_keyword(self, keyword, count=20):
		pass
