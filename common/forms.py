import json
from django.conf import settings
from common.cleaners import ValueCleaner

class Form(object):
	def __init__(self):
		self.m_request = None
		self.m_data = None
		self.m_fields = {}
		self.m_rfields = {}
		self.m_values = {}
		self.m_errors = {}


	def request(self):
		return self.m_request


	def data(self):
		return self.m_data


	def errors(self):
		return self.m_errors


	def values(self):
		return self.m_values


	def result(self):
		result = {}
		for key in self.m_values:
			result[self.m_rfields[key]] = self.m_values[key]
		return result


	def set_value(self, key, val):
		fkey = self.m_fields[key].get('name', key)
		self.m_rfields[fkey] = key
		self.m_values[fkey] = val


	## find actual key and set error.
	def set_error(self, key, err):
		rkey = self.m_rfields.get(key, key)
		self.m_errors[rkey] = err
		if key == rkey:
			logging.warning('key not found in request', key)


	def parseJson(self, request):
		return self.parse(request, True)


	def parseForm(self, request):
		return self.parse(request, False)


	def parse(self, request, is_json=True):
		print('parsing ....')
		self.m_request = request
		if is_json == True:
			self.m_data = json.loads(request.body.decode('utf-8'))
		else:
			self.m_data = request.POST
		for key in self.m_data:
			if key in self.m_fields:
				self.set_value(key, self.m_data[key])
		return True


	def clean(self):
		print('cleaning ....')
		cleaner = ValueCleaner()
		for key in self.m_values:
			#cleaner = self.m_fields[key].get('cleaner', None)
			self.m_values[key] = cleaner(self.m_values[key])
		return True


	def validate(self):
		print('validating ....')
		is_valid = True
		for key in self.m_values:
			fkey = self.m_rfields[key]
			validator = self.m_fields[fkey].get('validator', None)
			if validator != None:
				error = validator()(self.m_values[key])
				if error != None:
					self.set_error(key, error)
					is_valid = False
		return is_valid


	def commit(self):
		return None



class CreateForm(Form):

	def commit(self):
		return self.save()

	def save(self):
		return None


class UpdateForm(Form):

	def commit(self):
		return self.update()

	def update(self):
		return None


class DeleteForm(Form):

	def commit(self):
		return self.delete()

	def delete(self):
		return None
