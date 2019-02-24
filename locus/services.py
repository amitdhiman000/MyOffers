from locus.models import Address
from base.serializers import (ModelValueSerializer, ModelValuesSerializer)


class AddressService(object):
    model = Address
    fields = ('id', 'name', 'person', 'phone', 'pincode', 'address', 'area', 'city', 'state', 'country', 'landmark', 'url', 'location')

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
    def address_by_user(klass, user):
        data = klass.model.fetch_by_user(user)
        return ModelValuesSerializer.json(data, klass.fields)
