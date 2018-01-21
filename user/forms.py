from base.forms import *
from base.validators import *
from user.models import User
from user import backends


model_fields = [
	{'name': 'id', 'validator': NoValidator},
	{'name': 'name', 'validator': NameValidator},
	{'name': 'password', 'validator': PasswordValidator},
	{'name': 'email', 'validator': EmailValidator},
	{'name': 'phone', 'validator': PhoneValidator},
]

form_fields = {
	## for html form
	'U_id': model_fields[0],
	'U_name': model_fields[1],
	'U_pass': model_fields[2],
	'U_email': model_fields[3],
	'U_phone': model_fields[4],
	## for json
	'id': model_fields[0],
	'name': model_fields[1],
	'pass': model_fields[2],
	'email': model_fields[3],
	'phone': model_fields[4],
}


class UserRegForm(CreateForm):

	def __init__(self):
		super().__init__()
		self.m_fields = form_fields

	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid
		email = self.model_value('email')
		if User.check_email(email):
			self.set_error('email', 'Email already in use')
			return False
		return True


	def save(self):
		print('saving ....')
		return User.create(self.model_values())



class UserUpdateForm(UpdateForm):

	def __init__(self):
		super().__init__()
		self.m_fields = form_fields


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid
		self.add_model_value('id', self.m_request.user.id)
		print(self.m_values)
		return True


	def update(self):
		print('saving ....')
		if User.update(self.model_values()):
			return self.result()
		else:
			return None



class UserSignInForm(Form):

	def __init__(self):
		super().__init__()
		self.m_fields = {
			'U_email': {'name':'email', 'validator':None},
			'U_pass': {'name':'password', 'validator':None},
			'email': {'name':'email', 'validator':None},
			'pass': {'name':'password', 'validator':None},
		}

	def validate(self):
		return super().validate()


	def commit(self):
		print('commiting....')
		model_values = self.model_values()
		email = model_values['email']
		passw = model_values['password']
		print(email, passw)
		user = backends.auth_user(email, passw)
		if (user != None):
			backends.login(self.request(), user)
		else:
			self.set_error('email', 'Email or password is wrong!!')
		return user
