class ModelValueSerializer(object):

    def __init__(self, query_set):
        self.query_set = query_set

    def json(self):
        count = self.query_set.count()
        print(count)
        output = {}
        if count <= 1:
            output = {}
            json_obj = {}
            obj = query_set.first()
            for field in self.Meta.fields:
                json_obj.update({field:getattr(obj, field, '')})
            output = json_obj
        elif count > 1:
            output = []
            for obj in self.query_set:
                json_obj = {}
                for field in self.Meta.fields:
                    json_obj.update({field:getattr(obj, field, '')})
                output.append(json_obj)
        return output
