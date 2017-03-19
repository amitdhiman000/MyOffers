from datetime import datetime
from django.utils import timezone

from user.models import Area
from offer.models import Offer

## debug
import traceback
from pprint import pprint


class OfferControl(object):

	def parseRequest(self, request):
		post = request.POST
		files = request.FILES
		try:
			self.m_valid = False
			self.m_values = {}
			self.m_errors = {}
			self.m_offer = Offer()
 
			print('files : '+ str(len(files)))
			file = files.get('product_image')
			#print('image name : '+file.name)

			self.m_offer.product_image = file
			self.m_offer.product_name = post.get('product_name', '').strip(' \t\n\r')
			self.m_offer.discount = post.get('discount', '').strip(' \t\n\r')
			date_str1 = post.get('start_date', '').strip(' \t\n\r')
			date_str2 = post.get('expire_date', '').strip(' \t\n\r')
			tz = timezone.get_current_timezone()
			self.m_offer.start_date = tz.localize(datetime.strptime(date_str1, "%Y/%m/%d"))
			self.m_offer.expire_date = tz.localize(datetime.strptime(date_str2, "%Y/%m/%d"))
			self.m_offer.fk_user = request.user
			self.m_location = post.get('location', '').strip(' \t\n\r')
			# save values for session
			self.m_values['product_name'] = self.m_offer.product_name
			self.m_values['discount'] = self.m_offer.discount
			self.m_values['start_date'] = date_str1
			self.m_values['expire_date'] = date_str2
			self.m_values['location'] = self.m_location
			return True
		except:
			print('Failed to parse request')
			traceback.print_exc()
			return False

	def get_errors(self):
		return self.m_errors

	def get_values(self):
		return self.m_values

	def validate(self):
		print('start validating')
		valid = True
		if self.m_offer.product_name == '':
			valid = False
			self.m_errors['product_name'] = '*product name cannot be empty'

		if self.m_offer.discount == '':
			valid = False
			self.m_errors['discount'] = '*Discount cannot be empty'

		if self.m_offer.start_date < timezone.now():
			valid = False
			self.m_errors['start_date'] = '*Start date cannot be before today'

		if self.m_offer.expire_date < timezone.now():
			valid = False
			self.m_errors['expire_date'] = '*Expire date cannot be before today'

		if self.m_offer.start_date > self.m_offer.expire_date:
			valid = False
			self.m_errors['start_date'] = '*Start date cannot be before expire date'

		try:
			name, pin = self.m_location.split("(")
			pin = pin.split(")")[0]
			print('area name : '+name)
			print('area pin : '+pin)
			area = Area.get(name, pin)
			if area == None:
				valid = False
				self.m_errors['location'] = 'location not found'
			else:
				self.m_offer.fk_area = area
		except:
			print('failed to get area')
			traceback.exc()
			self.m_errors['location'] = '*Invalid location'
			valid = False

		self.m_valid = valid
		return valid

	def register(self):
		if self.m_valid:
			Offer.create(self.m_offer)
			return self.m_offer
		else:
			return None
