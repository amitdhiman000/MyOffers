import json
from common.forms import *
from common.validators import *


user_fields = {
	## for html form
	'U_id': {'name': 'id', 'validator': NoValidator},
	'U_name': {'name': 'name', 'validator': NameValidator},
	'U_pass': {'name': 'password', 'validator': PasswordValidator},
	'U_email': {'name': 'email', 'validator': EmailValidator},
	'U_phone': {'name': 'phone', 'validator': PhoneValidator},
	## for json
	'id': {'name': 'id', 'validator': NoValidator},
	'name': {'name': 'name', 'validator': NameValidator},
	'pass': {'name': 'password', 'validator': PasswordValidator},
	'email': {'name': 'email', 'validator': EmailValidator},
	'phone': {'name': 'phone', 'validator': PhoneValidator},
}


class UserRegForm(Form):

	def __init__(self):
		super().__init__(self)
		self.m_fields = user_fields

	def parseJson(self, request):
		self.m_data = json.loads(request.body.decode('utf-8'))
		super().parse()


	def parseForm(self, request):
		self.m_data = request.POST
		super().parse()


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid
		values = self.model_values()
		email = values.get('email', '')
		#if User.check_email():
		return True


	def save(self):
		values = self.model_values()
		return User.create(values)
