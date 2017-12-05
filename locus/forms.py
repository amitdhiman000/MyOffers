import json
from .models import Area, Address
from user.models import User
from common.apputil import Klass
from common.forms import Form

class AddressForm(Form):
    model = Address
    form_fields = {'A_name': 'name',
        'A_location':'location',
        'A_phone':'phone',
        'A_address':'address',
        'A_pincode':'pincode',
        'A_landmark':'landmark'
        }


    def parseHtml(self, request):
        content = request.META.get('CONTENT_TYPE')
        print(content)
        data = request.POST
        for key,val in self.form_fields.items():
            self._values[val] = data[key]


    def parseJson(self, request):
        content = request.META.get('CONTENT_TYPE')
        #content = request.META.get('HTTP_ACCEPT')
        print(content)
        self._values = {'pincode': 0, 'phone': '',
                        'name': '', 'pincode': '',
                        'landmark': '', 'latitude':'',
                        'longitude':'', 'area': None,
                        'user': None,
                        }
        data = json.loads(request.body.decode('utf-8'))
        for key,val in self.form_fields.items():
            if val in data:
                self._values[val] = data[val]

        print(self._values)
        area = Area.fetch_by_pincode(self._values['pincode'])
        print(area.pincode)
        if (area != None):
            self._values['area'] = area

        user = User.fetch_user(Klass(email='amitdhiman000@gmail.com'))
        if (user != None):
            self._values['user'] = user

        return True


    def clean(self):
        return True


    def validate(self):
        self._cleaned_values = Address().__dict__
        print(self._cleaned_values)
        return True


    def save(self):
        return self.model.create(self._values)
