import re
from datetime import datetime
from django.utils import timezone


class Validator(object):
    def __call__(self, value, *args):
        return 'Not validated'


class NoValidator(Validator):
    def __call__(self, value, *args):
        return None


class NameValidator(Validator):
    def __call__(self, value, *args):
        name = value
        error = None
        if name is None or name == '':
            error = '*Name is required'
        else:
            length = len(name)
            if length > 50:
                error = '*Name is too long'
            elif length < 3:
                error = '*Name is too short'
            # some more checks required
        return error


class EmailValidator(Validator):
    def __call__(self, value, *args):
        email = value
        error = None
        if email is None or email == '':
            error = '*Email is required'
        else:
            match = re.match('^[_a-z0-9-]+(.[_a-z0-9-]+)*@[a-z0-9-]+(.[a-z0-9-]+)*(.[a-z]{2,4})$', email)
            if match is None:
                error = '*Invalid email address'
        return error


class PhoneValidator(Validator):
    def __call__(self, value, *args):
        phone = value
        error = None
        if phone is None or phone == '':
            error = '*phone can\'t be empty'
        else:
            length = len(phone)
            if length != 10:
                error = '*phone should be 10 digits long'
        return error


class PasswordValidator(Validator):
    def __call__(self, value, *args):
        passw = value
        error = None
        if passw is None or passw == '':
            error = '*password can\'t be empty'
        else:
            length = len(passw)
            '''
            if length > 20:
                error = '*password is too long'
            elif length < 3:
                error = '*Password is too short'
            '''
        return error


class PriceValidator(Validator):
    def __call__(self, value, *args):
        price = value
        error = None
        if price is None or price == '':
            error = '*Price is required'
        else:
            try:
                temp = int(price)
                if temp < 0:
                    error = '*Price cannot be negative'
            except Exception as ex:
                error = '*Ileagal price value'
        # some more checks required
        return error


class DiscountValidator(Validator):
    def __call__(self, value, *args):
        discount = value
        error = None
        if discount is None or discount == '':
            error = '*Discount filed is required'
        else:
            try:
                temp = int(discount)
                if temp > 100 or temp < 0:
                    error = '*Discount value expected 0 to 99'
            except Exception as ex:
                error = '*Ileagal value not allowed'
        # some more checks required
        return error


class DescriptionValidator(Validator):
    def __call__(self, value, *args):
        desc = value
        error = None
        if desc is None or desc == '':
            error = '*Description cannot be empty'
        else:
            length = len(desc)
            if length > 200:
                error = '*Too long description'
            elif length < 3:
                error = '*Too short description'
        return error


class WebsiteValidator(Validator):
    def __call__(self, value, *args):
        website = value
        error = None
        if website is None or website == '':
            pass
            # error = '*Website is required'
        else:
            pass
            # some more checks required
        return error


class DateValidator(Validator):
    def __call__(self, value, *args):
        date = value
        error = None
        if date is None or date == '':
            error = '*Date value is missing'
        else:
            try:
                tz = timezone.get_current_timezone()
                start = tz.localize(datetime.strptime(date, "%Y/%m/%d"))
            except Exception as ex:
                print(ex)
                error = 'Invalid date format'
        return error
