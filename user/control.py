import re
from .models import User
from .models import FileUpload
from . import backends
from background_task import background

from pprint import pprint


## run after 60 seconds
@background(schedule=1*60)
def clear_file_upload(user_id, upload_id):
	print('clear_file_upload :: start')
	user = User.get_user_by_id(user_id)
	FileUpload.remove(upload_id, user)
	print('clear_file_upload :: done')
	#user.email_user('Here is a notification', 'You have been notified')


class BaseControl(object):

	def parseRequest(post):
		return True

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
		return None


class UserSignInControl(BaseControl):
	def parseRequest(self, post):
		self.m_valid = True
		self.m_errors = {}
		self.m_values = {}
		self.m_user = User()
		try:
			self.m_user.email = post.get('email', '').strip(' \t\n\r')
			self.m_user.passw = post.get('pass', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			self.m_errors.update({'user': 'Invalid request format'})
			return False

		return True


	def signin(self, request):
		user = backends.auth_user(self.m_user.email, self.m_user.passw)
		if user != None:
			backends.login(request, user)
			return True
		self.m_errors.update({'user': 'Email or password is wrong!!'})
		return False




class UserRegControl(BaseControl):
	def parseRequest(self, post):
		self.m_valid = True
		self.m_errors = {}
		self.m_values = {}
		self.m_user = User()
		try:
			self.m_user.name = post.get('name', '').strip(' \t\n\r')
			self.m_user.email = post.get('email', '').strip(' \t\n\r')
			self.m_user.password = post.get('pass', '').strip(' \t\n\r')
			self.m_user.phone = post.get('phone', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			return False

		# keep a copy of older values
		self.m_values['name'] = self.m_user.name
		self.m_values['email'] = self.m_user.email
		self.m_values['phone'] = self.m_user.phone
		return True

	def clean(self):
		return True
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
				is_duplicate = User.objects.filter(email=self.m_user.email).exists()
				if is_duplicate:
					valid = False
					self.m_errors['email'] = '*Email already in use, Please try reset password'

		# check for password
		if self.m_user.password is None or self.m_user.password == '':
			valid = False
			self.m_errors['pass'] = '*password can\'t be empty'
		else:
			length = len(self.m_user.password)
			'''
			if length > 20:
				valid = False
				self.m_errors['pass'] = '*password is too long'
			elif length < 3:
				valid = False
				self.m_errors['pass'] = '*Password is too short'
			'''

		# check for phone
		if self.m_user.phone is None or self.m_user.phone == '':
			valid = False
			self.m_errors['phone'] = '*phone can\'t be empty'
		else:
			length = len(self.m_user.phone)
			if length != 10:
				valid = False
				self.m_errors['phone'] = '*phone should be 10 digits long'

		self.m_valid = valid
		return valid

	def register(self):
		return User.create(self.m_user)



class UserFileUploadControl(BaseControl):
	def parseRequest(self, request):
		self.m_errors = {}
		self.m_valid = True
		self.m_file = None
		self.m_user = request.user
		if request.FILES == None:
			self.m_errors['upload'] = 'No file attached'
			self.m_valid = False
			return False
		else:
			for key in request.FILES:
				self.m_file = request.FILES[key]
				break
			pprint('file : '+self.m_file.name)
		return True


	def validate(self):
		if self.m_valid == False:
			return self.m_valid

		print('validating')
		valid = True

		user = User.get_user(self.m_user)
		if user != None:
			self.m_user = user
		else:
			self.m_errors['upload'] = 'Invalid user'
			valid = False

		self.m_valid = valid
		return self.m_valid


	def register(self):
		upload = FileUpload.create(self.m_file, self.m_user)
		if upload != None:
			clear_file_upload(self.m_user.pk, upload.id)
		else:
			m_errors['upload'] = 'File upload server error, try again'
		return upload
