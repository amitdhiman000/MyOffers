import re
from user.models import User

class Validator(object):
    def __init__(self):
        pass

    def __call__(self, field):
        pass


class UserValidator(object):
	def validateName(self, name):
		error = None
		if name == None or name == '':
			error = '*Name is required'
		else:
			length = len(name)
			if length > 50:
				error = '*Name is too long'
			elif length < 3:
				error = '*Name is too short'
			#some more checks required
		return error


	def validateEmail(self, email):
		error = None
		if email == None or email == '':
			error = '*Email is required'
		else:
			match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)
			if match == None:
				print('Bad Email Address')
				error = '*Invalid email address'
			else:
				if User.objects.filter(email=email).exists():
					error = '*Email already in use, Please try reset password'
		return error


	def validatePhone(self, phone):
		error = None
		if phone == None or phone == '':
			error = '*phone can\'t be empty'
		else:
			length = len(phone)
			if length != 10:
				error = '*phone should be 10 digits long'
		return error


	def validatePassword(self, pass1, pass2):
		error = None
		if pass1 == None or pass1 == '':
			error = '*password can\'t be empty'
		elif pass1 != pass2:
			error = '*passwords donot match'
		else:
			length = len(pass1)
			'''
			if length > 20:
				error = '*password is too long'
			elif length < 3:
				error = '*Password is too short'
			'''
		return error



class OfferValidator(object):
	def validateName(self, name):
		error = None
		if name == None or name == '':
			error = '*Offer Name is required'
		else:
			length = len(name)
			if length > 50:
				error = '*Offer Name is too long'
			elif length < 3:
				error = '*Offer Name is too short'
			#some more checks required
		return error


	def validatePrice(self, price):
		error = None
		if price == None or price == '':
			error = '*Price is required'
		else:
			try:
				temp = int(price)
				if temp < 0:
					error = '*Price cannot be negative'
			except:
				error = '*Ileagal price value'
		#some more checks required
		return error


	def validateDiscount(self, discount):
		error = None
		if discount == None or discount == '':
			error = '*Discount filed is required'
		else:
			try:
				temp = int(discount)
				if temp > 100 or temp < 0:
					error = '*Discount value expected 0 to 99'
			except:
				error = '*Ileagal value not allowed'
		#some more checks required
		return error


	def validateDates(self, start, end):
		error = None
		if start == None or start == '' or end == None or end == '':
			error = '*Date field is missing'
		else:
			tz = timezone.get_current_timezone()
			start = tz.localize(datetime.strptime(start, "%Y/%m/%d"))
			if start < timezone.now():
				error = '*Start date cannot be before today'

			end = tz.localize(datetime.strptime(end, "%Y/%m/%d"))
			if end < timezone.now():
				error = '*Expire date cannot be before today'

			if start > end:
				error = '*Start date cannot be before expire date'
		return error



class BusinessValidator(object):
	def validateName(self, value):
		error = None
		if value == None or value == '':
			error = '*Business Name is required'
		else:
			length = len(value)
			if length > 50:
				error = '*Business Name is too long'
			elif length < 3:
				error = '*Business Name is too short'
			#some more checks required
		return error


	def validateCategory(self, value):
		error = None
		if value == None or value == '':
			pass
			#error = '*Website is required'
		else:
			pass
		#some more checks required
		return error


	def validateDescription(self, value):
		error = None
		if value == None or value == '':
			pass
			#error = '*Website is required'
		else:
			pass
		#some more checks required
		return error


	def validateWebsite(self, value):
		error = None
		if value == None or value == '':
			pass
			#error = '*Website is required'
		else:
			pass
		#some more checks required
		return error


class BaseValidator(object):
	@staticmethod
	def validate(value, *args, **kwargs):
		return 'not implemented'



class BusinessNameValidator(BaseValidator):
	@staticmethod
	def validate(value, *args, **kwargs):
		error = None
		if value == None or value == '':
			error = '*Business Name is required'
		else:
			length = len(value)
			if length > 50:
				error = '*Business Name is too long'
			elif length < 3:
				error = '*Business Name is too short'
			#some more checks required
		return error
