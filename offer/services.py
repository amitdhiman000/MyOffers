from offer.models import Offer
from base.serializers import (ModelValueSerializer, ModelValuesSerializer)


class OfferService(object):
    model = Offer

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
        return ModelValueSerializer.json(data)

    @classmethod
    def address_by_user(klass, user):
        data = klass.model.fetch_by_user(user)
        return ModelValuesSerializer.json(data)
