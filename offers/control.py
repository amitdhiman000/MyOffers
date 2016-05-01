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
			self.valid = False
			self.values = {}
			self.errors = {}
			self.offer = Offer()
			self.image = files.get('image', None)
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

		if self.image is None:
			valid = False
			self.errors['image'] = '*Image is Required'
		else:
			if self.image.size > 100*1024:
				valid = False
				self.errors['image'] = '*Image size should be less than 100KB'
			else:
				splited = self.image.content_type.rsplit('/')
				ext = splited[len(splited) - 1]
				self.image.ext = ext
				if splited[0] != 'image':
					valid = False
					self.errors['image'] = '*Not an image file'

		self.valid = valid
		return valid

	def register(self):
		if self.valid:
			print('ext : '+self.image.ext)
			self.offer.save()
			self.offer.image_name = str(self.offer.id)+'.'+self.image.ext
			print('image_name : '+self.offer.image_name)
			handle_uploaded_file(self.image, self.offer.image_name)
			self.offer.save(update_fields=['image_name'])
			return self.offer
		else:
			return None

	def delete(self):
		pass

