from datetime import datetime, timedelta
from django.utils import timezone

from locus.models import *
from user.models import User
from business.models import Category
from business.models import Business

from common.controls import BaseControl
from common.validators import BusinessValidator
from common.apputil import App_Slugify

## debug
import traceback
from pprint import pprint
import logging


class AddressControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST;
		self.m_user = request.user;
		self.m_address = Address()
		try:
			self.m_address.name = post.get('A_name', '').strip(' \t\n\r')
			self.m_address.phone = post.get('A_phone', '').strip(' \t\n\r')
			self.m_address.pincode = post.get('A_pincode', '').strip(' \t\n\r')
			self.m_address.address = post.get('A_address', '').strip(' \t\n\r')
			self.m_address.location = post.get('A_location', '').strip(' \t\n\r')
		except Exception as e:
			logging.error(e);
			self.m_errors['error'] = 'Failed to parse request data'
			return False

		# keep a copy of older values
		self.m_values['A_name'] = self.m_address.name
		self.m_values['A_phone'] = self.m_address.phone
		self.m_values['A_pincode'] = self.m_address.pincode
		self.m_values['A_address'] = self.m_address.address
		self.m_values['A_location'] = self.m_address.location
		return True


	def validate(self):
		validator = BusinessValidator()
		error = validator.validateName(self.m_address.name)
		if error != None:
			self.m_errors['A_name'] = error

		self.m_address.area = Area.fetch_by_pincode(self.m_address.pincode)
		if self.m_address.area == None:
			self.m_errors['A_area'] = 'No such area found'

		self.m_address.user = User.fetch_user(self.m_user)
		if self.m_address.user == None:
			self.m_errors['A_name'] = 'No such user found'

		loc = self.m_address.location.split(',')
		if len(loc) == 2:
			self.m_address.latitude = loc[0]
			self.m_address.longitude = loc[1]

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		address = Address.create(self.m_address, self.m_user)
		if address == None:
			self.m_errors['error'] = 'Database internal Error'
		return address
