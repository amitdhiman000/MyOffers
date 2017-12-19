from django.conf import settings
from django.db import models
from datetime import datetime
from django.utils.translation import ugettext as _

from user.models import User
from locus.models import Address
# Create your models here.
import logging


# Business types
class Category(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=30)
	details = models.CharField(max_length=50)
	parent = models.ForeignKey("self", null=True, on_delete=models.DO_NOTHING)

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
		except Exception as e:
			logging.warning(e)
			return False


	@classmethod
	def fetch_first_level(klass):
		return klass.objects.filter(parent__name="All")


	@classmethod
	def fetch_all(klass):
		return klass.objects.all()


	@classmethod
	def fetch_by_id(klass, id):
		try:
			return klass.objects.get(id=id)
		except Exception as e:
			logging.debug(e)
			return None


	@classmethod
	def fetch_by_name(klass, name):
		try:
			return klass.objects.get(name=name)
		except Exception as e:
			logging.warning(e)
			return None


	@classmethod
	def fetch_children(klass, name):
		return klass.objects.filter(parent__name=name)



# Business
class Business(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50, blank=False)
	about = models.CharField(max_length=100, blank=False)
	website = models.CharField(max_length=100, blank=True)
	fk_category = models.ForeignKey(Category, on_delete=models.CASCADE)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
	#fk_address = models.ForeignKey(Address)


	@classmethod
	def create(klass, values):
		obj = klass.objects.get_or_create(**values)[0]
		return obj


	@classmethod
	def update(klass, values):
		try:
			business_id = values['id']
			obj = klass.objects.filter(id=business_id).update(**values)
			return obj
		except Exception as ex:
			logging.error(ex)
		return None


	@classmethod
	def remove(klass, values):
		try:
			obj = klass.objects.filter(**values)
			obj.delete()
			return True
		except Exception as ex:
			logging.error(ex)
			return False


	@classmethod
	def fetch_by_id(klass, id):
		try:
			return klass.objects.get(id=id)
		except Exception as e:
			logging.error(e)
			return None


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
		except Exception as e:
			logging.warning(e)
			return False


	@classmethod
	def fetch_by_business(klass, business):
		db_objs = klass.objects.filter(fk_business=business)
		return db_objs
