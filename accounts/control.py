import re
from .models import Consumer, Vendor

class BaseControl(object):

	def __init__(self):
		pass
		# do nothing

	def get_errors(self):
		return self.m_errors

	def get_values(self):
		return self.m_values

	def clean(self):
		pass
		#do nothing
		return True

	def validate(self):
		# do nothing
		return True

	def register(self):
		# do nothing
		return True


class ConsumerRegControl(BaseControl):
	
	def __init__(self, post=None):
		if post is None:
			raise ValueError("post data is None")

		self.m_valid = True
		self.m_errors = {}
		self.m_values = {}
		self.m_user = Consumer()
		self.m_user.name = post.get('name', '').strip(' \t\n\r')
		self.m_user.email = post.get('email', '').strip(' \t\n\r')
		pass1 = post.get('pass1', '').strip(' \t\n\r')
		pass2 = post.get('pass2', '').strip(' \t\n\r')
		self.m_user.password = pass1
		if pass1 != pass2:
			self.m_valid = False
			self.m_errors['pass2'] = '*Passwords do not match!'


		# keep a copy of older values
		self.m_values['name'] = self.m_user.name
		self.m_values['email'] = self.m_user.email

	def clean(self):
		pass
		#self.m_user.name = self.m_user.name.strip(' \t\n\r')

	def validate(self):
		valid = self.m_valid

		# check for user name
		if self.m_user.name is None or self.m_user.name == '':
			valid = False
			self.m_errors['name'] = '*Name is required'
		else:
			length = len(self.m_user.name)
			if length > 50:
				valid = False
				self.m_errors['name'] = '*Name is too long'
			elif length < 3:
				valid = False
				self.m_errors['name'] = '*Name is too short'
			#some more checks required

		# check for email
		if self.m_user.email is None or self.m_user.email == '':
			valid = False
			self.m_errors['email'] = '*Email is required'
		else:
			match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.m_user.email)
			if match is None:
				print('Bad Email Address')
				valid = False
				self.m_errors['email'] = '*Invalid email address'
			else:
				is_duplicate = Consumer.objects.filter(email=self.m_user.email).exists()
				if is_duplicate:
					valid = False
					self.m_errors['email'] = '*Email already in use, Please try reset password'

		# check for password
		if self.m_user.password is None or self.m_user.password == '':
			valid = False
			self.m_errors['pass1'] = '*password can\'t be empty'
		else:
			length = len(self.m_user.password)
			if length > 20:
				valid = False
				self.m_errors['pass1'] = '*password is too long'
			elif length < 3:
				valid = False
				self.m_errors['pass1'] = '*Password is too short'

		self.m_valid = valid
		return valid

	def register(self):
		self.m_user.add_consumer()
		return self.m_user


class VendorRegControl(BaseControl):

	def __init__(self, post=None):
		if post is None:
			raise ValueError("post data is None")