from datetime import datetime
from .models import Offer

# Create your tests here.

class OfferControl(object):

	def __init__(self, post=None):
		if post is None:
			raise ValueError("post data is None")
		else:
			self.valid = False
			self.values = {}
			self.errors = {}
			self.offer = Offer()
			self.offer.product_name = post.get('product_name', '').strip(' \t\n\r')
			self.offer.discount = post.get('discount', '').strip(' \t\n\r')
			date_str1 = post.get('start_date', '').strip(' \t\n\r')
			self.offer.start_date = datetime.strptime(date_str1, "%d-%m-%Y")
			date_str2 = post.get('expire_date', '').strip(' \t\n\r')
			self.offer.expire_date = datetime.strptime(date_str2, "%d-%m-%Y")

			self.values['product_name'] = self.offer.product_name
			self.values['discount'] = self.offer.discount
			self.values['start_date'] = date_str1
			self.values['expire_date'] = date_str2

	def get_errors(self):
		return self.errors

	def get_values(self):
		return self.values

	def validate(self):
		valid = True
		if self.offer.product_name == '':
			valid = False
			self.errors['product_name'] = '*product name cannot be empty'

		if self.offer.discount == '':
			valid = False
			self.errors['discount'] = '*Discount cannot be empty'

		if self.offer.start_date < datetime.now():
			valid = False
			self.errors['start_date'] = '*Start date cannot be before today'

		if self.offer.expire_date < datetime.now():
			valid = False
			self.errors['expire_date'] = '*Expire date cannot be before today'

		self.valid = valid
		return valid

	def register(self):
		if self.valid:
			self.offer.register()
			return self.offer
		else:
			return None

	def delete(self):
		pass

