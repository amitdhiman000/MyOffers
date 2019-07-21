from django.db import models
from base.models import (CRUDModel, CRUDModelWithUrl)
from user.models import UserModel

from django.utils.translation import ugettext as _
import logging


class CountryModel(CRUDModel):
    name = models.CharField(max_length=50, blank=False)

    class Meta:
        verbose_name = _('country')
        verbose_name_plural = _('countries')

    @classmethod
    def fetch_or_create(klass, name):
        return klass.create({'name': name})


class StateModel(CRUDModel):
    name = models.CharField(max_length=50, blank=True)
    fk_country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('state')
        verbose_name_plural = _('states')

    @classmethod
    def fetch_or_create(klass, state_name, country):
        print('Amit Dhiman', state_name, country)
        return klass.create({'name': state_name, 'fk_country': country})


class CityModel(CRUDModel):
    name = models.CharField(max_length=50)
    fk_state = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    fk_country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('city')
        verbose_name_plural = _('cities')

    @classmethod
    def fetch_or_create(klass, city_name, state, country):
        return klass.create({'name': city_name, 'fk_state': state, 'fk_country': country})

    @classmethod
    def fetch_by_name(klass, city_name, state_name, country_name):
        try:
            return klass.objects.get(name=city_name, fk_state__name=state_name, fk_country__name=country_name)
        except Exception as ex:
            logging.error(ex)
        return None


class AreaModel(CRUDModel):
    name = models.CharField(max_length=50, blank=True)
    pincode = models.CharField(max_length=10, blank=True)
    fk_city = models.ForeignKey(CityModel, on_delete=models.CASCADE)
    fk_state = models.ForeignKey(StateModel, on_delete=models.CASCADE)
    fk_country = models.ForeignKey(CountryModel, on_delete=models.CASCADE)

    class Meta:
        verbose_name = _('area')
        verbose_name_plural = _('areas')

    @classmethod
    def fetch_or_create(klass, area_name, area_pin, city, state, country):
        values = {
            'name': area_name,
            'pincode': area_pin,
            'fk_city': city,
            'fk_state': state,
            'fk_country': country
        }
        return klass.create(values)

    @classmethod
    def fetch_by_pincode(klass, area_pin):
        try:
            return klass.objects.filter(pincode=area_pin)
        except Exception as e:
            logging.error(e)
        return None

    @classmethod
    def fetch_by_city(klass, city):
        try:
            return klass.objects.filter(fk_city__name=city)
        except Exception as e:
            logging.error(e)
        return None

    @classmethod
    def fetch_by_match(klass, keyw):
        print('key is : '+keyw)
        query = klass.objects.annotate(city=models.F('fk_city__name')).filter(name__istartswith=keyw).values('name', 'pin', 'city')[:20]
        # query = klass.objects.annotate(city_name=models.F('fk_city__city_name')).filter(area_name__icontains=keyw).values('area_name', 'area_pin', 'city_name')
        return query


class AddressModel(CRUDModelWithUrl):
    name = models.CharField(max_length=50, blank=False)
    person = models.CharField(max_length=20, blank=True)
    phone = models.CharField(max_length=10, blank=True)
    address = models.CharField(max_length=50, blank=False)
    landmark = models.CharField(max_length=50, blank=True)
    latitude = models.CharField(max_length=10, blank=True)
    longitude = models.CharField(max_length=10, blank=True)
    fk_area = models.ForeignKey(AreaModel, on_delete=models.CASCADE)
    fk_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    flags = models.CharField(max_length=10, default='')

    class Meta:
        verbose_name = _('address')
        verbose_name_plural = _('address')

    def url(self):
        return '/locus/address/' + str(self.id) + '/'

    @classmethod
    def queryset(klass):
        # fields = ('id', 'name', 'person', 'phone', 'pincode', 'address', 'area', 'city', 'state', 'country')
        return klass.objects.annotate(
        pincode=models.F('fk_area__pincode'),
        area=models.F('fk_area__name'),
        city=models.F('fk_area__fk_city__name'),
        state=models.F('fk_area__fk_state__name'),
        country=models.F('fk_area__fk_country__name'),
        location=models.functions.Concat('latitude', models.Value(','), 'longitude'))

    @classmethod
    def fetch_all(klass):
        return klass.queryset()

    @classmethod
    def fetch_by_id(klass, id_):
        return klass.queryset().filter(id=id_)

    @classmethod
    def fetch_by_user(klass, user):
        return klass.queryset().filter(fk_user=user)


class Location(CRUDModel):
    name = models.CharField(max_length=50, blank=False)
    latitude = models.CharField(max_length=10)
    longitude = models.CharField(max_length=10)

    @classmethod
    def fetch_by_geo(klass, latitude, longitude):
        obj = klass.objects.get_or_create(latitude=latitude, longitude=longitude)
        return obj

    @classmethod
    def fetch_by_user(klass, user):
        return klass.objects.filter(fk_user=user)
