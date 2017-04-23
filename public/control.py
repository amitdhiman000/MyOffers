import re
from control import BaseControl
from user.models import User
from public.models import UserMessage
from public.models import GuestMessage


class MessageControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		self.m_valid = True
		self.m_errors = {}
		self.m_values = {}
		self.m_user = request.user
		self.m_msg = None

		try:
			if self.m_user.is_loggedin():
				self.m_msg = UserMessage()
				self.m_msg.text = post.get('text', '').strip(' \t\n\r')
			else:
				self.m_msg = GuestMessage()
				self.m_msg.name = post.get('name', '').strip(' \t\n\r')
				self.m_msg.email = post.get('email', '').strip(' \t\n\r')
				self.m_msg.phone = post.get('phone', '').strip(' \t\n\r')
				self.m_msg.text = post.get('text', '').strip(' \t\n\r')
				# keep a copy of older values
				self.m_values['name'] = self.m_msg.name
				self.m_values['email'] = self.m_msg.email
				self.m_values['phone'] = self.m_msg.phone
		except:
			import traceback
			traceback.print_exc()
			return False

		self.m_values['text'] = self.m_msg.text
		return True

	def clean(self):
		return True
		#self.m_msg.name = self.m_msg.name.strip(' \t\n\r')

	def validate(self):
		valid = self.m_valid

		if self.m_user.is_loggedin():
			# get user
			user = User.get_user(self.m_user)
			self.m_msg.fk_user = user
		else:
			# check for user name
			if self.m_msg.name == None or self.m_msg.name == '':
				valid = False
				self.m_errors['name'] = '*Name is required'
			else:
				length = len(self.m_msg.name)
				if length > 50:
					valid = False
					self.m_errors['name'] = '*Name is too long'
				elif length < 3:
					valid = False
					self.m_errors['name'] = '*Name is too short'
				#some more checks required

			# check for email
			if self.m_msg.email == None or self.m_msg.email == '':
				valid = False
				self.m_errors['email'] = '*Email is required'
			else:
				match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.m_msg.email)
				if match == None:
					print('Bad Email Address')
					valid = False
					self.m_errors['email'] = '*Invalid email address'
				'''
				else:
					is_duplicate = User.objects.filter(email=self.m_msg.email).exists()
					if is_duplicate:
						valid = False
						self.m_errors['email'] = '*Email already in use, Please try reset password'
				'''

			# check for phone
			if self.m_msg.phone == None or self.m_msg.phone == '':
				# okay phone is not mendatory
				#valid = False
				#self.m_errors['phone'] = '*phone can\'t be empty'
				pass
			else:
				length = len(self.m_msg.phone)
				if length != 10:
					valid = False
					self.m_errors['phone'] = '*phone should be 10 digits long'

		# check for text
		print(self.m_msg.text)
		if self.m_msg.text == None or self.m_msg.text == '':
			valid = False
			self.m_errors['text'] = '*message can\'t be empty'
			
		self.m_valid = valid
		return valid

	def register(self):
		if self.m_user.is_loggedin():
			return UserMessage.create(self.m_msg)
		else:
			return GuestMessage.create(self.m_msg)

