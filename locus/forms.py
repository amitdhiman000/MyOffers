from base.forms import *
from locus.models import (Area, Address)
from user.models import User

import logging

model_fields = {
	'id':{'name':'id', 'validator': None},
	'name':{'name':'name', 'validator': None},
	'person':{'name':'person', 'validator': None},
	'phone':{'name':'phone', 'validator': None},
	'pincode':{'name':'pincode', 'validator': None},
	'address':{'name':'address', 'validator': None},
	'landmark':{'name':'landmark', 'validator': None},
	'location':{'name':'location', 'validator': None},
}

form_fields = {
	## form fields
	'A_id': model_fields['id'],
	'A_name': model_fields['name'],
	'A_pname': model_fields['person'],
	'A_phone': model_fields['phone'],
	'A_pincode': model_fields['pincode'],
	'A_address': model_fields['address'],
	'A_landmark': model_fields['landmark'],
	'A_location': model_fields['location'],

	## json fields
	'id': model_fields['id'],
	'name': model_fields['name'],
	'pname': model_fields['person'],
	'phone': model_fields['phone'],
	'pincode': model_fields['pincode'],
	'address': model_fields['address'],
	'landmark': model_fields['landmark'],
	'location': model_fields['location'],
}


class AddressRegForm(CreateForm):
	model = Address

	def __init__(self):
		super().__init__()
		self.m_fields = form_fields


	def validate(self):
		super().validate()

		#location = self.model_value('location')
		location = self.del_model_value('location')
		if location != None:
			try:
				loc = location.split(',')
				if len(loc) == 2:
					self.add_model_value('latitude', loc[0])
					self.add_model_value('longitude', loc[1])
			except Exception as ex:
				logging.error(ex)
				self.set_error('location', 'Failed to parse location')
				self.m_valid = False

		pincode = self.model_value('pincode')
		address = self.model_value('address')
		if pincode != '':
			areas = Area.fetch_by_pincode(pincode)
			if areas.exists():
				final_area = areas.first()
				for area in areas:
					print(area.name, area.pincode)
					if address.find(area.name):
						final_area = area
				self.add_model_value('fk_area', final_area)
				self.del_model_value('pincode')
			else:
				self.set_error('pincode', "We don't serve this area yet")
		else:
			self.set_error('pincode', 'Pincode is required')

		self.add_model_value('fk_user', self.request().user)

		return self.valid()


	def save(self):
		print(self.model_values())
		result = self.model.create(self.model_values())
		if result[1] == False:
			self.set_error('error', 'Address already exists!!')
			return None
		return result[0]



class AddressUpdateForm(UpdateForm):
	model = Address

	def __init__(self):
		super().__init__()
		self.m_fields = form_fields


	def validate(self):
		super().validate()
		return self.valid()


	def update(self):
		return self.model.update(self.model_values())



class AddressDeleteForm(DeleteForm):
	model = Address

	def __init__(self):
		super().__init__()
		self.m_fields = {
			'A_id': {'name':'id', 'validator':None},
			'id': {'name':'id', 'validator':None},
		}


	def validate(self):
		super().validate()
		self.add_model_value('fk_user', self.request().user)
		return self.valid()


	def delete(self):
		print(self.model_values())
		return self.model.remove(self.model_values())
