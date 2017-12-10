from common.cleaners import ValueCleaner

class Form(object):
    def __init__(self):
        self.m_fields = {}
        self.m_data = {}
        self.m_values = {}
        self.m_errors = {}
        self.m_model_values = {}


    def errors(self):
        return self.m_errors


    def data(self):
        return self.m_data


    def values(self):
        return self.m_values


    def parse(self, request):
        for key in self.m_data.keys():
            if key in self.m_fields:
                self.m_values[key] = self.m_data[key]
        return True


    def clean(self):
        cleaner = ValueCleaner()
        for key in self.m_values.keys():
            #cleaner = self.m_fields[key].get('cleaner', None)
            self.m_values[key] = cleaner(self.m_values[key])
        return True


    def validate(self):
        is_valid = True
        for key in self.m_values.keys():
            validator = self.m_fields[key].get('validator', None)
            if validator != None:
                error = validator()(self.m_values[key])
                if error != None:
                    self.m_errors[key] = error
                    is_valid = False
        return is_valid


    def model_values(self):
        if len(self.m_model_values) > 0:
            return self.m_model_values
        for key in self.m_values.keys():
            name = self.m_fields.get('name', None)
            if name != None:
                self.m_model_values[name] = self.m_values[key]
        return m_model_values


    def commit(self):
        return None



class CreateForm(object):

    def commit(self):
        return self.save()

    def save(self):
        return None


class UpdateForm(object):

    def commit(self):
        return self.update()

    def update(self):
        return None


class DeleteForm(object):

    def commit(self):
        return self.delete()

    def delete(self):
        return None
