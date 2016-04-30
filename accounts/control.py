
import re
from .models import Consumer, Vendor

class BaseControl(object):

	def __init__(self):
		pass
		# do nothing

	def get_errors(self):
		return self.errors

	def get_values(self):
		return self.values

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

		self.valid = True
		self.errors = {}
		self.values = {}
		self.user = Consumer()
		self.user.name = post.get('name', '').strip(' \t\n\r')
		self.user.email = post.get('email', '').strip(' \t\n\r')
		pass1 = post.get('pass1', '').strip(' \t\n\r')
		pass2 = post.get('pass2', '').strip(' \t\n\r')
		self.user.password = pass1
		if pass1 != pass2:
			self.valid = False
			self.errors['pass2'] = '*Passwords do not match!'


		# keep a copy of older values
		self.values['name'] = self.user.name
		self.values['email'] = self.user.email

	def clean(self):
		pass
		#self.user.name = self.user.name.strip(' \t\n\r')

	def validate(self):
		valid = self.valid

		# check for user name
		if self.user.name is None or self.user.name == '':
			valid = False
			self.errors['name'] = '*Name is required'
		else:
			length = len(self.user.name)
			if length > 50:
				valid = False
				self.errors['name'] = '*Name is too long'
			elif length < 3:
				valid = False
				self.errors['name'] = '*Name is too short'
			#some more checks required

		# check for email
		if self.user.email is None or self.user.email == '':
			valid = False
			self.errors['email'] = '*Email is required'
		else:
			match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.user.email)
			if match is None:
				print('Bad Email Address')
				valid = False
				self.errors['email'] = '*Invalid email address'
			else:
				is_duplicate = Consumer.objects.filter(email=self.user.email).exists()
				if is_duplicate:
					valid = False
					self.errors['email'] = '*Email already in use, Please try reset password'

		# check for password
		if self.user.password is None or self.user.password == '':
			valid = False
			self.errors['pass1'] = '*password can\'t be empty'
		else:
			length = len(self.user.password)
			if length > 20:
				valid = False
				self.errors['pass1'] = '*password is too long'
			elif length < 3:
				valid = False
				self.errors['pass1'] = '*Password is too short'

		return valid

	def register(self):
		self.user.add_consumer()
		return self.user


class VendorRegControl(BaseControl):

	def __init__(self, post=None):
		if post is None:
			raise ValueError("post data is None")