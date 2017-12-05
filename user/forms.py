import json
from common.forms import Form

class UserRegForm(Form):
    _fields = ('id', 'name', 'email', 'pass', 'phone')

    def parseJson(self, request):
        data = json.loads(request.body.decode('utf-8'))
        for key in self._fields:
            if key in data:
                self._values[key] = data[key]


    def parseForm(self, request):
        pass


    def clean(self):
        pass


    def validate(self):
        pass


    def save(self):
        return None


    def delete(self):
        return False
