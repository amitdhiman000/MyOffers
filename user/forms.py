import json
from common.forms import *
from common.validators import *
from user.models import User


model_fields = {
	'id': {'name': 'id', 'validator': NoValidator},
	'name': {'name': 'name', 'validator': NameValidator},
	'password': {'name': 'password', 'validator': PasswordValidator},
	'email': {'name': 'email', 'validator': EmailValidator},
	'phone': {'name': 'phone', 'validator': PhoneValidator},
}

form_fields = {
	## for html form
	'U_id': 'id',
	'U_name': 'name',
	'U_pass': 'password',
	'U_email': 'email',
	'U_phone': 'phone',
	## for json
	'id': 'id',
	'name': 'name',
	'pass': 'password',
	'email': 'email',
	'phone': 'phone',
}


class UserRegForm(CreateForm):

	def __init__(self):
		super().__init__()
		self.m_form_fields = form_fields
		self.m_model_fields = model_fields

	def parseJson(self, request):
		self.m_data = json.loads(request.body.decode('utf-8'))
		return super().parse()


	def parseForm(self, request):
		self.m_data = request.POST
		return super().parse()


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid
		email = self.values().get('email', '')
		if User.check_email(email):
			self.set_error('email', 'Email already in use')
			return False
		return True


	def save(self):
		print('saving ....')
		return User.create(self.values())
