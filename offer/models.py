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
	business_name = models.CharField(max_length=30)
	business_desc = models.CharField(max_length=50)

	class Meta:
		verbose_name = _('business')
		verbose_name_plural= _('business')

	def __str__(self):
		return self.business_name

	@classmethod
	def create(klass, name, desc):
		obj = klass(business_name=name, business_desc=desc)
		obj.save()


# offers table for new offers
class Offer(models.Model):
	P_id = models.BigAutoField(primary_key=True)
	P_name = models.CharField(max_length=30, blank=False)
	P_image = models.FileField(upload_to=user_files_dir)
	P_price = models.IntegerField(default=100) ## MRP
	P_discount = models.IntegerField(default=0)
	P_discount_price = models.IntegerField(default=100)
	P_created = models.DateTimeField(default=timezone.now)
	P_start_date = models.DateTimeField(default=timezone.now)
	P_expire_date = models.DateTimeField(default=days_ahead(5))
	P_slug = models.SlugField(unique=True)
	P_details = models.TextField()
	fk_user = models.ForeignKey(User)
	fk_area = models.ForeignKey(Area)

	class Meta:
		verbose_name = _('offer')
		verbose_name_plural= _('offers')

	def __str__(self):
		return self.P_name

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
			db_obj['url'] = '/offer/'+db_obj['P_slug']
		return db_objs

	@classmethod
	def add_url_to_objs(klass, db_objs):
		for db_obj in db_objs:
			db_obj.url = '/offer/'+db_obj.P_slug
		return db_objs

	@classmethod
	def add_url_to_obj(klass, db_obj):
		if db_obj:
			db_obj.url = '/offer/'+db_obj.P_slug
		return db_obj


	@classmethod
	def get_all(klass):
		db_objs = klass.objects.all()
		return klass.add_url_to_objs(db_objs)

	@classmethod
	def get_by_id(klass, id):
		try:
			db_objs = klass.objects.get(P_id=id)
			return klass.add_url_to_objs(db_objs)
		except:
			print('Failed to get product')
			traceback.print_exc()
			return None


	@classmethod
	def get_by_slug(klass, slug):
		try:
			db_obj = klass.objects.get(P_slug=slug)
			return klass.add_url_to_obj(db_obj)
		except:
			print('Failed to get product')
			traceback.print_exc()
			return None

	@classmethod
	def get_match(klass, keyw):
		try:
			db_objs = klass.objects.filter(P_name__contains=keyw).values('P_id', 'P_name', 'P_slug')[:10]
			return klass.add_url_to_dict(db_objs)
		except:
			traceback.print_exc()
			return []


	def get_by_location(self, location, count=20):
		pass

	def get_by_keyword(self, keyword, count=20):
		pass

