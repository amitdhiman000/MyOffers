from datetime import datetime
from django.utils import timezone

from user.models import User
from user.models import Area
from user.models import FileUpload
from offer.models import Offer

## debug
import traceback
from pprint import pprint


class OfferControl(object):

	def parseRequest(self, request):
		post = request.POST
#		files = request.FILES
		try:
			self.m_valid = False
			self.m_values = {}
			self.m_errors = {}
			self.m_file_id = None
			self.m_user = request.user
			self.m_offer = Offer()
 
			if request.is_ajax():
				self.m_file_id = post.get('files')
			else:
				self.m_offer.product_image = request.FILES['product_image']

			self.m_offer.product_name = post.get('product_name', '').strip(' \t\n\r')
			self.m_offer.discount = post.get('discount', '').strip(' \t\n\r')
			self.m_offer.start_date = post.get('start_date', '').strip(' \t\n\r')
			self.m_offer.expire_date = post.get('expire_date', '').strip(' \t\n\r')
			self.m_area = post.get('area', '').strip(' \t\n\r')
			# save values for session
			self.m_values['product_name'] = self.m_offer.product_name
			self.m_values['discount'] = self.m_offer.discount
			self.m_values['start_date'] = self.m_offer.start_date
			self.m_values['expire_date'] = self.m_offer.expire_date
			self.m_values['area'] = self.m_area
			return True
		except:
			self.m_errors['request'] = 'Failed to parse request'
			print('Failed to parse request')
			traceback.print_exc()
			return False

	def get_errors(self):
		return self.m_errors

	def get_values(self):
		return self.m_values

	def validate(self):
		valid = True
		print('start validating')

		if self.m_offer.product_name == '':
			valid = False
			self.m_errors['product_name'] = '*product name cannot be empty'

		if self.m_offer.discount == '':
			valid = False
			self.m_errors['discount'] = '*Discount cannot be empty'

		tz = timezone.get_current_timezone()
		try:
			self.m_offer.start_date = tz.localize(datetime.strptime(self.m_offer.start_date, "%Y/%m/%d"))
			if self.m_offer.start_date < timezone.now():
				valid = False
				self.m_errors['start_date'] = '*Start date cannot be before today'
		except:
			valid = False
			self.m_errors['start_date'] = 'Invalid date format'

		try:
			self.m_offer.expire_date = tz.localize(datetime.strptime(self.m_offer.expire_date, "%Y/%m/%d"))
			if self.m_offer.expire_date < timezone.now():
				valid = False
				self.m_errors['expire_date'] = '*Expire date cannot be before today'
		except:
			valid = False
			self.m_errors['expire_date'] = 'Invalid date format'

		if self.m_offer.start_date > self.m_offer.expire_date:
			valid = False
			self.m_errors['start_date'] = '*Start date cannot be before expire date'

		try:
			name, pin = self.m_area.split("(")
			pin = pin.split(")")[0]
			print('area name : '+name)
			print('area pin : '+pin)
			area = Area.get(name, pin)
			if area != None:
				self.m_offer.fk_area = area
			else:
				valid = False
				self.m_errors['area'] = 'location not found'
		except:
			valid = False
			self.m_errors['area'] = '*Invalid area'
			print('failed to get area')
			traceback.exc()

		self.m_offer.fk_user = User.get_user(self.m_user)
		if self.m_file_id != None and self.m_file_id != '':
			upload = FileUpload.get_file(int(self.m_file_id), self.m_offer.fk_user)
			if upload != None:
				pprint(self.m_file_id)
				pprint(upload)
				self.m_offer.product_image = upload.file
			else:
				valid = False
				self.m_errors['product_image'] = 'File attachement expires'
		else:
			valid = False
			self.m_errors['product_image'] = 'No files attached'

		self.m_valid = valid
		return self.m_valid

	def register(self):
		if self.m_valid:
			offer = Offer.create(self.m_offer)
			if offer != None:
				FileUpload.mark_used(self.m_file_id, self.m_user)
			return self.m_offer
		else:
			return None

