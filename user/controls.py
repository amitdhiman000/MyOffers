from user.models import User
from upload.models import FileUpload
from common.controls import BaseControl
from common.validators import UserValidator

from . import backends
## debug
import traceback
from pprint import pprint


class UserSignInControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		self.m_request = request
		self.m_user = User()
		try:
			self.m_user.email = post.get('U_email', '').strip(' \t\n\r')
			self.m_user.passw = post.get('U_pass', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			self.m_errors['error'] = 'Invalid request format'
			return False
		return True


	def validate(self):
		user = backends.auth_user(self.m_user.email, self.m_user.passw)
		if user != None:
			self.m_user = user
		else:
			self.m_errors['U_email'] = 'Email or password is wrong!!'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if self.m_valid == False:
			return None
		backends.login(self.m_request, self.m_user)
		return self.m_user



class UserSignUpControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		self.m_user = User()
		try:
			self.m_user.name = post.get('U_name', '').strip(' \t\n\r')
			self.m_user.email = post.get('U_email', '').strip(' \t\n\r')
			self.m_user.password = post.get('U_pass', '').strip(' \t\n\r')
			self.m_user.phone = post.get('U_phone', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			return False

		# keep a copy of older values
		self.m_values['U_name'] = self.m_user.name
		self.m_values['U_email'] = self.m_user.email
		self.m_values['U_phone'] = self.m_user.phone
		return True


	def clean(self):
		return True


	def validate(self):
		validator = UserValidator()

		error = validator.validateName(self.m_user.name)
		if error != None:
			self.m_errors['U_name'] = error

		error = validator.validateEmail(self.m_user.email)
		if error != None:
			self.m_errors['U_email'] = error

		error = validator.validatePassword(self.m_user.password, self.m_user.password)
		if error != None:
			self.m_errors['U_pass'] = error

		error = validator.validatePhone(self.m_user.phone)
		if error != None:
			self.m_errors['U_phone'] = error

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		return User.create(self.m_user)



class UserControlFactory(object):
	@classmethod
	def getControl(request):
		field = request.POST.get('field_name', '')
		controls = {
			'U_name': UserNameControl,
			'U_email': UserEmailControl,
			'U_pass': UserPassControl,
			'U_phone': UserPhoneControl,
			'': BaseControl,
		}
		return controls[field]



class UserNameControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		self.m_user = request.user;
		try:
			self.m_val = post.get('U_name', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			return False
		return True


	def validate(self):
		validator = UserValidator()
		error = validator.validateName(self.m_val)
		if error != None:
			self.m_errors['U_name'] = error

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if self.m_valid == False:
			return None
		return User.update_name(self.m_val, self.m_user)



class UserEmailControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		self.m_user = request.user;
		try:
			self.m_val = post.get('U_email', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			return False
		return True


	def validate(self):
		validator = UserValidator()
		error = validator.validateEmail(self.m_val)
		if error != None:
			self.m_errors['U_email'] = error

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if self.m_valid == False:
			return None
		return User.update_email(self.m_val, self.m_user)


class UserPhoneControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		self.m_user = request.user;
		try:
			self.m_val = post.get('U_phone', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			return False
		return True


	def validate(self):
		validator = UserValidator()
		error = validator.validateEmail(self.m_val)
		if error != None:
			self.m_errors['U_phone'] = error

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if self.m_valid == False:
			return None
		return User.update_phone(self.m_val, self.m_user)



class UserPasswordControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		self.m_user = request.user;
		try:
			self.m_pass0 = post.get('U_pass0', '').strip(' \t\n\r')
			self.m_pass1 = post.get('U_pass1', '').strip(' \t\n\r')
			self.m_pass2 = post.get('U_pass2', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			return False
		return True


	def validate(self):
		if User.check_password(self.m_pass0, self.m_user) == False:
			self.m_errors['error'] = 'Wrong old password'

		validator = UserValidator()
		error = validator.validatePassword(self.m_pass1, self.m_pass2)
		if error != None:
			self.m_errors['U_pass'] = error

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if self.m_valid == False:
			return None
		return User.update_password(self.pass1, self.m_user)
