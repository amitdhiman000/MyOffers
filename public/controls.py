import re
from user.models import User
from public.models import UserMessage
from public.models import GuestMessage
from common.controls import BaseControl
from common.validators import *

def is_number(s):
	try:
		int(s)
		return True
	except ValueError:
		return False


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
				self.m_msg.title = post.get('title', '').strip(' \t\n\r')
				self.m_msg.text = post.get('text', '').strip(' \t\n\r')
			else:
				self.m_msg = GuestMessage()
				self.m_msg.name = post.get('name', '').strip(' \t\n\r')
				self.m_msg.email = post.get('email', '').strip(' \t\n\r')
				self.m_msg.phone = self.m_msg.email
				self.m_msg.title = post.get('title', '').strip(' \t\n\r')
				self.m_msg.text = post.get('text', '').strip(' \t\n\r')
				# keep a copy of older values
				self.m_values['name'] = self.m_msg.name
				self.m_values['email'] = self.m_msg.email
				self.m_values['title'] = self.m_msg.title
				self.m_values['text'] = self.m_msg.text
		except:
			import traceback
			traceback.print_exc()
			return False

		self.m_values['text'] = self.m_msg.text
		return True


	def clean(self):
		return True


	def validate(self):
		valid = self.m_valid

		validator = UserValidator()
		if self.m_user.is_loggedin():
			# get user
			user = User.get_user(self.m_user)
			self.m_msg.fk_user = user
		else:
			# check for user name
			error = validator.validateName(self.m_msg.name)
			if error != None:
				self.m_errors['name'] = error

			# check for email
			if self.m_msg.email == None or self.m_msg.email == '':
				valid = False
				self.m_errors['email'] = '*Email or Phone is required'
			else:
				match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.m_msg.email)
				if match != None:
					# valid email
					self.m_msg.phone = ""
				elif is_number(self.m_msg.phone):
					if len(self.m_msg.phone) < 10:
						print('Bad Phone Number')
						valid = False
					else:
						self.m_msg.email = ""
				else:
					print('Bad Email Address')
					valid = False
					self.m_errors['email'] = '*Invalid email address'


		# check for phone
		if self.m_msg.title == None or self.m_msg.title == '':
			# okay title is not mendatory
			#valid = False
			#self.m_errors['title'] = '*title can\'t be empty'
			pass

		# check for text
		print(self.m_msg.text)
		if self.m_msg.text == None or self.m_msg.text == '':
			valid = False
			self.m_errors['text'] = '*message can\'t be empty'

		self.m_valid = valid
		return valid


	def execute(self):
		if self.m_user.is_loggedin():
			return UserMessage.create(self.m_msg)
		else:
			return GuestMessage.create(self.m_msg)
