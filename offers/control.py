from datetime import datetime
from .models import Offer
from django.conf import settings

# Create your tests here.

def handle_uploaded_file(image_file, file_name='file'):
    with open(settings.STATIC_DIR+'/images/offers/'+file_name, 'wb+') as destination:
        for chunk in image_file.chunks():
            destination.write(chunk)

class OfferControl(object):

	def __init__(self, post=None, files=None):
		if post is None:
			raise ValueError("post data is None")
		else:
			self.m_valid = False
			self.m_values = {}
			self.m_errors = {}
			self.m_offer = Offer()
			self.m_image = files.get('image', None)
			self.m_offer.product_name = post.get('product_name', '').strip(' \t\n\r')
			self.m_offer.discount = post.get('discount', '').strip(' \t\n\r')
			date_str1 = post.get('start_date', '').strip(' \t\n\r')
			self.m_offer.start_date = datetime.strptime(date_str1, "%d-%m-%Y")
			date_str2 = post.get('expire_date', '').strip(' \t\n\r')
			self.m_offer.expire_date = datetime.strptime(date_str2, "%d-%m-%Y")

			self.m_values['product_name'] = self.m_offer.product_name
			self.m_values['discount'] = self.m_offer.discount
			self.m_values['start_date'] = date_str1
			self.m_values['expire_date'] = date_str2

	def get_errors(self):
		return self.m_errors

	def get_values(self):
		return self.m_values

	def validate(self):
		valid = True
		if self.m_offer.product_name == '':
			valid = False
			self.m_errors['product_name'] = '*product name cannot be empty'

		if self.m_offer.discount == '':
			valid = False
			self.m_errors['discount'] = '*Discount cannot be empty'

		if self.m_offer.start_date < datetime.now():
			valid = False
			self.m_errors['start_date'] = '*Start date cannot be before today'

		if self.m_offer.expire_date < datetime.now():
			valid = False
			self.m_errors['expire_date'] = '*Expire date cannot be before today'

		if self.m_image is None:
			valid = False
			self.m_errors['image'] = '*Image is Required'
		else:
			if self.m_image.size > 100*1024:
				valid = False
				self.m_errors['image'] = '*Image size should be less than 100KB'
			else:
				splited = self.m_image.content_type.rsplit('/')
				ext = splited[len(splited) - 1]
				self.m_image.ext = ext
				if splited[0] != 'image':
					valid = False
					self.m_errors['image'] = '*Not an image file'

		self.m_valid = valid
		return valid

	def register(self):
		if self.m_valid:
			print('ext : '+self.m_image.ext)
			self.m_offer.save()
			self.m_offer.image_name = str(self.m_offer.id)+'.'+self.m_image.ext
			print('image_name : '+self.m_offer.image_name)
			handle_uploaded_file(self.m_image, self.m_offer.image_name)
			self.m_offer.save(update_fields=['image_name'])
			return self.m_offer
		else:
			return None

	def delete(self):
		pass

