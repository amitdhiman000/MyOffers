from base.serializers import *
from locus.models import Address
from business.models import BusinessAddressMap

class BusinessService(object):
    model = BusinessAddressMap
    fields = ('id', 'name', 'person', 'phone', 'pincode', 'address', 'area', 'city', 'state', 'country', 'landmark', 'url')

    @classmethod
    def timestamp(klass, key):
        return klass.model.timestamp(key)


    @classmethod
    def address(klass):
        data = klass.model.fetch_all()
        return ModelValueSerializer.json(data)


    @classmethod
    def address_by_id(klass, id_):
        data = klass.model.fetch_by_id(id_)
        print(data)
        return ModelValueSerializer.json(data, klass.fields)


    @classmethod
    def fetch_by_business(klass, b_id, user):
        data = klass.model.fetch_by_business(b_id, user)
        return ModelValuesSerializer.json(data, klass.fields)
