from django.conf import settings
from django.db import models
from base.models import CRUDModel
from datetime import datetime
from django.utils.translation import ugettext as _

from user.models import User
from locus.models import Address
# Create your models here.
import logging


# Business types
class Category(CRUDModel):
	name = models.CharField(max_length=30)
	details = models.CharField(max_length=50)
	parent = models.ForeignKey("self", null=True, on_delete=models.DO_NOTHING)

	class Meta:
		verbose_name = _('category')
		verbose_name_plural= _('categories')


	def __str__(self):
		return self.name


	@classmethod
	def fetch_by_name(klass, name):
		try:
			return klass.objects.get(name=name)
		except Exception as ex:
			logging.warning(ex)
		return None


	@classmethod
	def fetch_first_level(klass):
		return klass.objects.filter(parent__name="All")


	@classmethod
	def fetch_children(klass, name):
		return klass.objects.filter(parent__name=name)



# Business
class Business(CRUDModel):
	name = models.CharField(max_length=50, blank=False)
	about = models.CharField(max_length=100, blank=False)
	website = models.CharField(max_length=100, blank=True)
	fk_category = models.ForeignKey(Category, on_delete=models.CASCADE)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)
	#fk_address = models.ForeignKey(Address)


	@classmethod
	def create(klass, values):
		try:
			obj = klass.objects.create(**values)
			return obj
		except Exception as ex:
			logging.error(ex)
		return None


	@classmethod
	def fetch_by_user(klass, user):
		return klass.objects.filter(fk_user=user)



class BusinessAddressMap(CRUDModel):
	fk_business = models.ForeignKey(Business, on_delete=models.CASCADE)
	fk_address = models.ForeignKey(Address, on_delete=models.CASCADE)
