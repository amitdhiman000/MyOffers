import os
from django.conf import settings
from django.db import models
from datetime import datetime
from datetime import timedelta
from django.utils import timezone
from django.utils.translation import ugettext as _
from user.models import Area
from user.models import User

# Create your models here.
def days_ahead(days=1):
	return timezone.now() + timezone.timedelta(days=days)

def user_product_dir(inst, filename):
	# file will be uploaded to MEDIA_ROOT/products/user_<id>/<filename>
	path = os.path.join(settings.MEDIA_PROCUCTS_DIR_NAME, 'user_{0}/{1}_{2}'.format(inst.fk_user.id, timezone.now(), filename))
	print(path)
	return path


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
	product_name = models.CharField(max_length=30, blank=False)
	product_image = models.FileField(upload_to=user_product_dir)
	discount = models.CharField(max_length=3)
	create_time = models.DateTimeField(default=timezone.now)
	start_date = models.DateTimeField(default=timezone.now)
	expire_date = models.DateTimeField(default=days_ahead(5))
	description = models.TextField()
	fk_user = models.ForeignKey(User)
	fk_area = models.ForeignKey(Area)

	class Meta:
		verbose_name = _('offer')
		verbose_name_plural= _('offers')

	def __str__(self):
		return self.product_name

	@classmethod
	def get_all(klass):
		return klass.objects.all()

	def get_by_location(self, location='bengaluru', count=20):
		pass

	def get_by_keyword(self, keyword='', count=20):
		pass

	@classmethod
	def create(klass, obj):
		obj.save()

	@classmethod
	def remove(klass, obj):
		try:
			db_obj = klass.objects.get(obj)
			db_obj.delete()
			return True
		except:
			print('failed to delete')
			return False

	@classmethod
	def get_match(klass, keyw):
		try:
			return klass.objects.annotate(name=models.F('product_name')).filter(product_name__contains=keyw).values('id', 'name')[:15]
		except:
			traceback.exc()
			return []
