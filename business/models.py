# from django.conf import settings
from django.db import models
from base.models import CRUDModel
from user.models import UserModel
from locus.models import AddressModel

from django.utils.translation import ugettext as _
import logging


# Business types
class CategoryModel(CRUDModel):
    name = models.CharField(max_length=30)
    details = models.CharField(max_length=50)
    parent = models.ForeignKey("self", null=True, on_delete=models.DO_NOTHING)

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

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
class BusinessModel(CRUDModel):
    name = models.CharField(max_length=50, blank=False)
    about = models.CharField(max_length=100, blank=False)
    website = models.CharField(max_length=100, blank=True)
    fk_category = models.ForeignKey(CategoryModel, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    # fk_address = models.ForeignKey(AddressModel)

    @classmethod
    def fetch_by_user(klass, user):
        return klass.objects.filter(fk_user=user)


class BusinessAddressMapModel(CRUDModel):
    fk_business = models.ForeignKey(BusinessModel, on_delete=models.CASCADE)
    fk_address = models.ForeignKey(AddressModel, on_delete=models.CASCADE)

    @classmethod
    def fetch_by_business(klass, b_id, user):
        linked = klass.objects.filter(fk_business=b_id).annotate(
        a_id = models.F('fk_address__id')).values_list('a_id', flat=True)
        return set(linked)
