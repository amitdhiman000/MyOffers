from locus.models import Address
from business.models import BusinessAddressMap
from base.serializers import (ModelValueSerializer, ModelValuesSerializer)


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
        return ModelValueSerializer.json(data, klass.fields)

    @classmethod
    def fetch_by_business(klass, b_id, user):
        addresses = Address.fetch_by_user(user)
        linked = klass.model.fetch_by_business(b_id, user)
        print(linked)
        for address in addresses:
            if address.id in linked:
                address.linked = True
            else:
                address.linked = False

        fields = klass.fields + ('linked',)
        json = ModelValuesSerializer.json(addresses, fields)
        return json

    @classmethod
    def fetch_by_linked(klass, b_id, user):
        linked = klass.model.fetch_by_business(b_id, user)
        return linked

    @classmethod
    def delete_by_id(klass, b_id, user):
        return klass.model.remove({'fk_business': b_id, 'fk_user': user})
