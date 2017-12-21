class ModelValueSerializer(object):

    @staticmethod
    def json(values_set):
        count = values_set.count()
        print(count)
        if count <= 1:
            return values_set.first()
        return list(values_set)


class ModelValuesSerializer(object):

    @staticmethod
    def json(values_set):
        return list(values_set)
