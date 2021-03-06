from django.db import models
from base.models import CRUDModel
from django.utils import timezone
from django.utils.translation import ugettext as _

from user.models import UserModel
from locus.models import AddressModel
from business.models import (CategoryModel, BusinessModel)
from base.apputil import App_UserFilesDir
import logging


# Create your models here.
def days_ahead(days=1):
    return timezone.now() + timezone.timedelta(days=days)


# offers table for new offers
class OfferModel(CRUDModel):
    slug = models.SlugField(unique=True)
    name = models.CharField(max_length=30, blank=False)
    details = models.TextField()
    image = models.FileField(upload_to=App_UserFilesDir)
    price = models.IntegerField(default=100)  # MRP
    discount = models.IntegerField(default=0)
    discount_price = models.IntegerField(default=100)
    start_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField(default=days_ahead(5))
    fk_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    fk_business = models.ForeignKey(BusinessModel, db_index=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('offer')
        verbose_name_plural = _('offers')

    def __str__(self):
        return self.name

    @property
    def url(self):
        return '/{0}/{1}/'.format('offer', self.slug)

    @staticmethod
    def _url_col():
        # return '/{0}/{1}/'.format('offer', slug)
        return models.functions.Concat(models.Value('/offer/'), 'slug', models.Value('/'), output_field=models.CharField())

    @classmethod
    def fetch_by_slug(klass, slug):
        try:
            db_obj = klass.objects.get(slug=slug)
            return db_obj
        except Exception as ex:
            logging.error(ex)
            return None

    @classmethod
    def fetch_by_match(klass, keyw):
        try:
            # db_objs = klass.objects.filter(name__contains=keyw).annotate(url=models.Value(klass.url_col(models.F('slug')), output_field=models.CharField())).values('id', 'name', 'slug', 'url')[:10]
            # db_objs = klass.objects.filter(name__contains=keyw).annotate(url1=models.ExpressionWrapper(models.F('slug'), output_field=models.CharField)).values('id', 'name', 'slug', 'url1')[:10]
            # db_objs = klass.objects.filter(name__contains=keyw).annotate(url=models.functions.Concat(models.Value('/offer/'), 'slug', models.Value('/'), output_field=models.CharField())).values('id', 'name', 'slug', 'url')[:10]
            db_objs = klass.objects.filter(name__contains=keyw).annotate(url=klass._url_col()).values('id', 'name', 'slug', 'url')[:10]
            return db_objs
        except Exception as ex:
            logging.error(ex)
        return []


class OfferCategoryMapModel(CRUDModel):
    fk_offer = models.ForeignKey(OfferModel, on_delete=models.CASCADE)
    fk_category = models.ForeignKey(CategoryModel, db_index=True, on_delete=models.CASCADE)


class OfferAddressMapModel(CRUDModel):
    fk_offer = models.ForeignKey(OfferModel, on_delete=models.CASCADE)
    fk_address = models.ForeignKey(AddressModel, db_index=True, on_delete=models.CASCADE)
