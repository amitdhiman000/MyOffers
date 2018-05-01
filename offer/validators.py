from base.validators import Validator
from django.utils import timezone
from datetime import datetime


class OfferNameValidator(Validator):
    def __call__(self, value, *args):
        name = value
        error = None
        if name is None or name == '':
            error = '*Offer Name is required'
        else:
            length = len(name)
            if length > 50:
                error = '*Offer Name is too long'
            elif length < 3:
                error = '*Offer Name is too short'
            # some more checks required
        return error


class OfferDatesValidator(Validator):
    def __call__(self, value, *args):
        start = value
        end = args[0]
        error = None
        if start is None or start == '' or end is None or end == '':
            error = '*Date value is missing'
        else:
            tz = timezone.get_current_timezone()
            start = tz.localize(datetime.strptime(start, "%Y/%m/%d"))
            if start < timezone.now():
                error = '*Start date cannot be before today'

            end = tz.localize(datetime.strptime(end, "%Y/%m/%d"))
            if end < timezone.now():
                error = '*Expire date cannot be before today'

            if start > end:
                error = '*Start date cannot be before expire date'
        return error
