from datetime import datetime, timedelta
from django.utils import timezone

from user.models import User
from locus.models import Area
from upload.models import FileUpload
from offer.models import Offer
from offer.models import Category
from offer.models import Business

from common.controls import BaseControl
from common.apputil import App_Slugify
from common.validators import OfferValidator

## debug
import traceback
from pprint import pprint



class BusinessControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST;
		self.m_user = request.user;
		self.m_business = Business()
		try:
			self.m_business.name = post.get('B_name', '').strip(' \t\n\r')
			self.m_business.desc = post.get('B_desc', '').strip(' \t\n\r')
			self.m_business.category = post.get('B_cat', '').strip(' \t\n\r')
			self.m_business.website = post.get('B_web', '').strip(' \t\n\r')
		except:
			import traceback
			traceback.print_exc()
			self.m_errors['error'] = 'Failed to parse request data'
			return False

		# keep a copy of older values
		self.m_values['B_name'] = self.m_business.name
		self.m_values['B_desc'] = self.m_business.desc
		self.m_values['B_cat'] = self.m_business.category
		self.m_values['B_web'] = self.m_business.website
		return True


	def validate(self):
		self.m_business.category = Category.fetch_by_id(self.m_business.category)
		if self.m_business.category == None:
			self.m_errors['error'] = 'No such category found'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None

		business = Business.create(self.m_business, self.m_user)
		if business == None:
			print('DB operation failed')
			self.m_errors['error'] = 'Database internal Error'
		return business



class OfferControl(BaseControl):
	def parseRequest(self, request):
		post = request.POST
		files = request.FILES
		self.m_category = None
		self.m_location = None
		self.m_files = None
		self.m_user = request.user
		self.m_offer = Offer()

		try:
			if request.is_ajax():
				self.m_files = post.get('files', '')
				if self.m_files == '':
					self.m_files = []
				else:
					self.m_files = [int(x) for x in self.m_files.split(',')]
				print('len : '+ str(len(self.m_files)))
			else:
				self.m_offer.image = files['P_image']

			self.m_offer.name = post.get('P_name', '').strip(' \t\n\r')
			self.m_offer.price = post.get('P_price', 0).strip(' \t\n\r')
			self.m_offer.discount = post.get('P_discount', 0).strip(' \t\n\r')
			self.m_offer.discount_price = post.get('P_discount_price', 0).strip(' \t\n\r')
			self.m_offer.start_date = post.get('P_start_date', '').strip(' \t\n\r')
			self.m_offer.expire_date = post.get('P_expire_date', '').strip(' \t\n\r')
			self.m_location = post.get('P_location', '').strip(' \t\n\r')
		except:
			self.m_errors['error'] = 'Failed to parse request'
			print('Failed to parse request')
			traceback.print_exc()
			return False

		# save values for session
		self.m_values['P_name'] = self.m_offer.name
		self.m_values['P_discount'] = self.m_offer.discount
		self.m_values['P_start_date'] = self.m_offer.start_date
		self.m_values['P_expire_date'] = self.m_offer.expire_date
		self.m_values['P_area'] = self.m_area
		return True


	def validate(self):
		valid = True
		temp = None
		print('start validating')

		validator = OfferValidator()
		error = validator.validateName(self.m_offer.name)
		if error != None:
			self.m_errors['P_name'] = error

		error = validator.validatePrice(self.m_offer.price)
		if error != None:
			self.m_errors['P_price'] = error

		error = validator.validateDiscount(self.m_offer.discount)
		if error != None:
			self.m_errors['P_discount'] = error


		error = validator.validatePrice(self.m_offer.discount_price)
		if error != None:
			self.m_errors['P_discount_price'] = error
		## FIXME :: later
		## special check for offer price margin


		error = validator.validateDates(self.m_offer.start_date, self.m_offer.expire_date)
		if error != None:
			self.m_errors['P_start_date'] = error


		self.m_offer.fk_user = User.get_user(self.m_user)
		if self.m_files != None and len(self.m_files) > 0:
			# FIXME later :: fetch support for multiple images
			pprint(self.m_files[0])
			upload = FileUpload.get_file(int(self.m_files[0]), self.m_offer.fk_user)
			if upload != None:
				pprint(upload)
				self.m_offer.image = upload.file
			else:
				valid = False
				self.m_errors['P_image'] = 'File attachement expires'
		else:
			valid = False
			self.m_errors['P_image'] = 'No files attached'


		#self.m_location = Location.get(self.m_user)
		self.m_location = Location.get_location_for_area(area)
		if self.m_location == None:
			valid = False
			self.m_errors['P_location'] = 'No location selected by you'

		if self.m_category < 0:
			valid = False
			self.m_errors['P_category'] = 'Ileagal value selected'


		## compute the slug
		slug = self.m_offer.name+'-by-'+self.m_offer.fk_user.name
		slug = App_Slugify(slug)
		if Offer.get_by_slug(slug) == None:
			self.m_offer.slug = slug
		else:
			self.m_errors['P_name'] = '*Product with this name is already present'

		self.m_valid = (len(self.m_errors) == 0)
		return self.m_valid


	def execute(self):
		if False == self.m_valid:
			return None
		offer = Offer.create(self.m_offer)
		if offer != None:
			OfferCategoryMap.create(offer, self.m_category)
			OfferLocationMap.create(offer, self.m_location)
			FileUpload.mark_used(self.m_files[0], self.m_user)
		else:
			self.m_errors['error'] = 'Database Failure'
		return offer
