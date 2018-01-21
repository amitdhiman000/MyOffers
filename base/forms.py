import json
from django.conf import settings
from base.cleaners import ValueCleaner


class Form(object):
	def __init__(self):
		self.m_request = None
		self.m_valid = False
		self.m_errors = {}
		self.m_values = {}
		self.m_fields = {}
		self.m_rfields = {}
		self.m_model_values = {}


	# return the request object
	def request(self):
		return self.m_request

	# return whether form is valid or not.
	def valid(self):
		return self.m_valid


	## returns the form errors and validating form
	def errors(self):
		return self.m_errors


	## return the form values got from client
	def values(self):
		return self.m_values


	## returns model values only for model usage
	def model_values(self):
		return self.m_model_values


	## set error for a model attr.
	def set_error(self, key, err):
		rkey = self.m_rfields.get(key, key)
		self.m_errors[rkey] = err
		self.m_valid = False
		if key == rkey:
			logging.warning('key not found in request', key)


	def process(self, request):
		return (self.parseForm(request)
				and self.clean()
				and self.validate())



	## parse the json request.
	def parseJson(self, request):
		return self.parse(request, True)


	## parse the html form POST request.
	def parseForm(self, request):
		return self.parse(request, False)


	## add new value for model
	def add_model_value(self, key, val):
		self.m_model_values[key] = val


	## del new value for model
	def del_model_value(self, key):
		try:
			return self.m_model_values.pop(key)
		except Exception as ex:
			logging.error(ex)
		return None


	## get model value for key
	def model_value(self, key):
		return self.m_model_values.get(key, '')


	## add value to model set/ only for internal usage.
	def make_model_value(self, key, val):
		fkey = self.m_fields[key].get('name', key)
		self.m_rfields[fkey] = key
		self.m_model_values[fkey] = val


	def parse(self, request, is_json=True):
		print('parsing ....')
		self.m_request = request
		if is_json == True:
			self.m_values = json.loads(request.body.decode('utf-8'))
		else:
			self.m_values = request.POST

		for key in self.m_values:
			if key in self.m_fields:
				self.make_model_value(key, self.m_values[key])
		return True


	def clean(self):
		print('cleaning ....')
		cleaner = ValueCleaner()
		for key in self.m_model_values:
			#cleaner = self.m_fields[key].get('cleaner', None)
			self.m_model_values[key] = cleaner(self.m_model_values[key])
		return True


	def validate(self):
		print('validating ....')
		self.m_valid = True
		for key in self.m_model_values:
			fkey = self.m_rfields[key]
			validator = self.m_fields[fkey].get('validator', None)
			if validator != None:
				error = validator()(self.m_model_values[key])
				if error != None:
					self.set_error(key, error)
		return self.valid()


	## sub classes are suppose to implement commit or equivalid methods.
	def commit(self):
		return None


	def result(self):
		result = {}
		for key in self.m_model_values:
			if key in self.m_rfields:
				result[self.m_rfields[key]] = self.m_model_values[key]
		return result



class CreateForm(Form):

	def clean(self):
		super().clean()
		## remove empty id
		if 'id' in self.m_model_values and self.m_model_values['id'] == '':
			self.m_model_values.pop('id')
		return True


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
