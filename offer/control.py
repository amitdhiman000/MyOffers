from datetime import datetime, timedelta
from django.utils import timezone

from user.models import User
from locus.models import Area
from upload.models import FileUpload
from offer.models import Offer
from apputil import App_Slugify

## debug
import traceback
from pprint import pprint


class OfferControl(object):

	def parseRequest(self, request):
		post = request.POST
		files = request.FILES
		self.m_valid = False
		self.m_values = {}
		self.m_errors = {}
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
			self.m_errors['request'] = 'Failed to parse request'
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

	def errors(self):
		return self.m_errors

	def values(self):
		return self.m_values

	def validate(self):
		valid = True
		temp = None
		print('start validating')

		if self.m_offer.name == '':
			valid = False
			self.m_errors['P_name'] = '*product name cannot be empty'

		try:
			temp = int(self.m_offer.price)
			if temp < 0:
				valid = False
				self.m_errors['P_price'] = '*Price cannot be negative'
		except:
			valid = False
			self.m_errors['P_price'] = '*Ileagal price value'

		try:
			temp = int(self.m_offer.discount)
			if temp > 100 or temp < 0:
				valid = False
				self.m_errors['P_discount'] = '*Discount value expected 0 to 99'
		except:
			valid = False
			self.m_errors['P_discount'] = '*Ileagal value not allowed'

		try:
			temp = int(self.m_offer.discount_price)
			if temp < 0:
				valid = False
				self.m_errors['P_discount_price'] = '*Price cannot be negative'
		except:
			valid = False
			self.m_errors['P_price'] = '*Ileagal discount price value'

		tz = timezone.get_current_timezone()
		self.m_offer.start_date = tz.localize(datetime.strptime(self.m_offer.start_date, "%Y/%m/%d"))
		if self.m_offer.start_date < timezone.now():
			valid = False
			self.m_errors['P_start_date'] = '*Start date cannot be before today'

		self.m_offer.expire_date = tz.localize(datetime.strptime(self.m_offer.expire_date, "%Y/%m/%d"))
		if self.m_offer.expire_date < timezone.now():
			valid = False
			self.m_errors['P_expire_date'] = '*Expire date cannot be before today'

		if self.m_offer.start_date > self.m_offer.expire_date:
			valid = False
			self.m_errors['P_start_date'] = '*Start date cannot be before expire date'


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
			valid = False
			self.m_errors['P_name'] = '*Product with this name is already present'

		self.m_valid = valid
		return self.m_valid

	def register(self):
		if self.m_valid:
			offer = Offer.create(self.m_offer)
			if offer != None:
				OfferCategoryMap.create(offer, self.m_category)
				OfferLocationMap.create(offer, self.m_location)
				FileUpload.mark_used(self.m_files[0], self.m_user)
			return self.m_offer
		else:
			return None
