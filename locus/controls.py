from datetime import datetime, timedelta
from django.utils import timezone

from locus.models import Address
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
			self.m_address.name = post.get('BA_name', '').strip(' \t\n\r')
			self.m_address.country = post.get('BA_country', '').strip(' \t\n\r')
			self.m_address.phone = post.get('BA_phone', '').strip(' \t\n\r')
			self.m_address.pincode = post.get('BA_pincode', '').strip(' \t\n\r')
			self.m_address.landmark = post.get('BA_landmark', '').strip(' \t\n\r')
			self.m_address.address = post.get('BA_address', '').strip(' \t\n\r')
		except Exception as e:
			logging.error(e);
			self.m_errors['error'] = 'Failed to parse request data'
			return False

		# keep a copy of older values
		self.m_values['BA_name'] = self.m_address.name
		self.m_values['BA_country'] = self.m_address.country
		self.m_values['BA_phone'] = self.m_address.phone
		self.m_values['BA_pincode'] = self.m_address.pincode
		self.m_values['BA_landmark'] = self.m_address.landmark
		self.m_values['BA_address'] = self.m_address.address
		return True


	def validate(self):
		validator = BusinessValidator()
		error = validator.validateName(self.m_address.name)
		if error != None:
			self.m_error['BA_name'] = error

		self.m_address.country = Country.fetch_by_name(self.m_address.country)
		if self.m_address.country == None:
			self.m_errors['BA_country'] = 'No such country found'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		address = Business.create(self.m_address, self.m_user)
		if address == None:
			self.m_errors['error'] = 'Database internal Error'
		return address
