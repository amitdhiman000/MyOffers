from base.validators import Validator

class BusinessNameValidator(Validator):
    def __call__(self, value, *args):
        name = value
        error = None
        if name == None or name == '':
            error = '*Business Name is required'
        else:
            length = len(name)
            if length > 50:
                error = '*Business Name is too long'
            elif length < 3:
                error = '*Business Name is too short'
            #some more checks required
        return error



class BusinessCategoryValidator(Validator):
    def __call__(self, value, *args):
        error = None
        if value == None or value == '':
            pass
            #error = '*Website is required'
        else:
            pass
        #some more checks required
        return error
