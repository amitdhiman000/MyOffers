from common.serializers import ModelValueSerializer
from .models import User


class UserService(object):
    model = User

    @classmethod
    def users(klass):
        users = klass.model.fetch_all()
        return ModelValueSerializer.json(users)

    @classmethod
    def user_by_id(klass, id_):
        user = klass.model.fetch_by_id(id_)
        return ModelValueSerializer.json(user)
