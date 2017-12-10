from datetime import datetime, timedelta
from django.utils import timezone

from user.models import User
from business.models import Category
from business.models import Business

from common.apputil import App_Slugify
from common.controls import BaseControl
from common.validators import *

## debug
import traceback
from pprint import pprint
import logging


class BusinessControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST;
		self.m_user = request.user;
		self.m_business = Business()
		try:
			self.m_business.name = post.get('B_name', '').strip(' \t\n\r')
			self.m_business.about = post.get('B_about', '').strip(' \t\n\r')
			self.m_business.category = post.get('B_category', '').strip(' \t\n\r')
			self.m_business.website = post.get('B_website', '').strip(' \t\n\r')
		except Exception as e:
			logging.error(e);
			self.m_errors['error'] = 'Failed to parse request data'
			return False

		# keep a copy of older values
		self.m_values['B_name'] = self.m_business.name
		self.m_values['B_about'] = self.m_business.about
		self.m_values['B_category'] = self.m_business.category
		self.m_values['B_website'] = self.m_business.website
		return True


	def validate(self):
		validator = BusinessValidator()
		error = validator.validateName(self.m_business.name)
		if error != None:
			self.m_error['B_name'] = error

		self.m_business.category = Category.fetch_by_id(self.m_business.category)
		if self.m_business.category == None:
			self.m_errors['B_category'] = 'No such category found'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		business = Business.create(self.m_business, self.m_user)
		if business == None:
			self.m_errors['error'] = 'Database internal Error'
		return business



class BusinessNameControl(BaseControl):
	m_field = 'B_name'
	m_id = 'B_id'
	def parseRequest(self, request):
		post = request.POST;
		self.m_user = request.user;
		self.m_val = None
		try:
			self.m_val = post.get(self.m_field, '').strip(' \t\n\r')
			self.m_business = post.get(self.m_id, '').strip(' \t\n\r')
		except Exception as e:
			logging.error(e);
			self.m_errors['error'] = 'Failed to parse request data'
			return False
		self.m_values[self.m_field] = self.m_val
		return True


	def validate(self):
		validator = BusinessValidator()
		error = validator.validateName(self.m_val)
		if error != None:
			self.m_error[self.m_field] = error

		self.m_business = Business.fetch_by_id(self.m_business)
		if self.m_business == None:
			self.m_error[self.m_field] = 'Business Item not found'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		name = Business.update_name(self.m_business, self.m_val)
		if name == None:
			self.m_errors['error'] = 'Database internal Error'
		return name


class BusinessCategoryControl(BaseControl):
	m_field = 'B_category'
	m_id = 'B_id'
	def parseRequest(self, request):
		post = request.POST;
		self.m_user = request.user;
		self.m_val = None
		try:
			self.m_val = post.get(self.m_field, '').strip(' \t\n\r')
			self.m_business = post.get(self.m_id, '').strip(' \t\n\r')
		except Exception as e:
			logging.error(e)
			self.m_errors['error'] = 'Failed to parse request data'
			return False
		self.m_values[self.m_field] = self.m_val
		return True


	def validate(self):
		validator = BusinessValidator()
		error = validator.validateCategory(self.m_val)
		if error != None:
			self.m_error[self.m_field] = error

		self.m_business = Business.fetch_by_id(self.m_business)
		if self.m_business == None:
			self.m_error[self.m_field] = 'Business Item not found'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		name = Business.update_category(self.m_business, self.m_val)
		if name == None:
			self.m_errors[self.m_field] = 'Database internal Error'
		return name



class BusinessAboutControl(BaseControl):
	m_field = 'B_about'
	m_id = 'B_id'
	def parseRequest(self, request):
		post = request.POST;
		self.m_user = request.user;
		self.m_val = None
		try:
			self.m_val = post.get(self.m_field, '').strip(' \t\n\r')
			self.m_business = post.get(self.m_id, '').strip(' \t\n\r')
		except Exception as e:
			logging.error(e);
			self.m_errors['error'] = 'Failed to parse request data'
			return False
		self.m_values[self.m_field] = self.m_val
		return True


	def validate(self):
		validator = BusinessValidator()
		error = validator.validateDescription(self.m_val)
		if error != None:
			self.m_error[self.m_field] = error

		self.m_business = Business.fetch_by_id(self.m_business)
		if self.m_business == None:
			self.m_error[self.m_field] = 'Business Item not found'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		name = Business.update_about(self.m_business, self.m_val)
		if name == None:
			self.m_errors[self.m_field] = 'Database internal Error'
		return name


class BusinessWebsiteControl(BaseControl):
	m_field = 'B_website'
	m_id = 'B_id'
	def parseRequest(self, request):
		post = request.POST;
		self.m_user = request.user;
		self.m_val = None
		try:
			self.m_val = post.get(self.m_field, '').strip(' \t\n\r')
			self.m_business = post.get(self.m_id, '').strip(' \t\n\r')
		except Exception as e:
			logging.error(e);
			self.m_errors['error'] = 'Failed to parse request data'
			return False
		self.m_values[self.m_field] = self.m_val
		return True


	def validate(self):
		validator = BusinessValidator()
		error = validator.validateWebsite(self.m_val)
		if error != None:
			self.m_error[self.m_field] = error

		self.m_business = Business.fetch_by_id(self.m_business)
		if self.m_business == None:
			self.m_error[self.m_field] = 'Business Item not found'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		name = Business.update_website(self.m_business, self.m_val)
		if name == None:
			self.m_errors[self.m_field] = 'Database internal Error'
		return name


class BusinessControlsFactory(object):
	@classmethod
	def getControl(klass, request):
		print(request.POST)
		field = ''
		controls = {
			'B_name': BusinessNameControl,
			'B_category': BusinessCategoryControl,
			'B_about': BusinessAboutControl,
			'B_website': BusinessWebsiteControl,
			'': BaseControl,
		}

		for key in request.POST:
			if key in controls.keys():
				field = key
				break

		print(field)
		return controls[field]()
