from common.cleaners import ValueCleaner

class Form(object):
    def __init__(self):
        self.m_form_fields = {}
        self.m_model_fields = {}
        self.m_rfields = {}
        self.m_data = {}
        self.m_values = {}
        self.m_errors = {}


    def data(self):
        return self.m_data


    def errors(self):
        return self.m_errors


    def values(self):
        return self.m_values


    def set_value(self, key, val):
        akey = self.m_form_fields[key]
        self.m_rfields[akey] = key
        self.m_values[akey] = val


    ## find actual key and set error.
    def set_error(self, key, err):
        rkey = self.m_rfields.get(key, key)
        self.m_errors[rkey] = err
        if key == rkey:
            logging.warning('key not found in request', key)


    def parse(self):
        print('parsing ....')
        for key in self.m_data.keys():
            if key in self.m_form_fields:
                self.set_value(key, self.m_data[key])
        return True


    def clean(self):
        print('cleaning ....')
        cleaner = ValueCleaner()
        for key in self.m_values.keys():
            #cleaner = self.m_fields[key].get('cleaner', None)
            self.m_values[key] = cleaner(self.m_values[key])
        return True


    def validate(self):
        print('validating ....')
        is_valid = True
        for key in self.m_values.keys():
            validator = self.m_model_fields[key].get('validator', None)
            if validator != None:
                error = validator()(self.m_values[key])
                if error != None:
                    self.set_error(key, error)
                    is_valid = False
        return is_valid


    def commit(self):
        return None



class CreateForm(Form):

    def commit(self):
        return self.save()

    def save(self):
        return None


class UpdateForm(Form):

    def commit(self):
        return self.update()

    def update(self):
        return None


class DeleteForm(Form):

    def commit(self):
        return self.delete()

    def delete(self):
        return None
