import types
# from django.core import serializers


class ModelValueSerializer(object):

    @staticmethod
    def json(query_set, fields=None):
        print('+ModelValueSerializer')
        if not query_set.exists():
            return None

        obj = query_set.first()
        for key, val in obj.ExtraFields.items():
            prop_method = getattr(obj, val)
            if isinstance(prop_method, types.MethodType):
                obj.__dict__[key] = prop_method()

        localdict = {}
        if fields is not None:
            for key in fields:
                localdict[key] = obj.__dict__[key]
        else:
            localdict = obj.__dict__
        return obj


class ModelValuesSerializer(object):

    @staticmethod
    def json(query_set, fields=None):
        print('+ModelValuesSerializer')
        datalist = []
        if not query_set.exists():
            return datalist

        # unwanted = set(query_set.first().__dict__.keys()) - set(fields)
        # print(unwanted)
        for obj in query_set:
            for key, val in obj.ExtraFields.items():
                prop_method = getattr(obj, val)
                if isinstance(prop_method, types.MethodType):
                    print('method found')
                    obj.__dict__[key] = prop_method()

            localdict = {}
            if fields is not None:
                for key in fields:
                    localdict[key] = obj.__dict__[key]
            else:
                localdict = obj.__dict__
            datalist.append(localdict)
        return datalist
