from base.forms import *
from base.validators import *
from business.validators import *
from business.models import (Business, Category)


model_fields = {
	'id':{'name': 'id', 'validator': NoValidator},
	'name':{'name': 'name', 'validator': BusinessNameValidator},
	'about':{'name': 'about', 'validator': DescriptionValidator},
	'website':{'name': 'website', 'validator': WebsiteValidator},
	'category':{'name': 'fk_category', 'validator': BusinessCategoryValidator},
}

form_fields = {
	## for html form
	'B_id': model_fields['id'],
	'B_name': model_fields['name'],
	'B_about': model_fields['about'],
	'B_website': model_fields['website'],
	'B_category': model_fields['category'],
	## for json
	'id': model_fields['id'],
	'name': model_fields['name'],
	'about': model_fields['about'],
	'website': model_fields['website'],
	'category': model_fields['category'],
}


class BusinessRegForm(CreateForm):

	def __init__(self):
		super().__init__()
		self.m_fields = form_fields


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid

		cat = Category.fetch_by_id(self.model_value('fk_category'))
		if cat != None:
			self.add_model_value('fk_category', cat)
		else:
			self.set_error('fk_category', 'Category not found')

		self.add_model_value('fk_user', self.request().user)
		return self.valid()


	def save(self):
		print('saving ....')
		print(self.model_values())
		return Business.create(self.model_values())



class BusinessUpdateForm(UpdateForm):

	def __init__(self):
		super().__init__()
		self.m_fields = form_fields


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid
		print(self.m_model_values)
		return True


	def update(self):
		print('saving ....')
		if Business.update(self.model_values()):
			return self.result()
		else:
			return None



class BusinessDeleteForm(DeleteForm):

	def __init__(self):
		super().__init__()
		self.m_fields = {
			'U_id': {'name':'id', 'validator':None},
			'id': {'name':'id', 'validator':None},
		}


	def validate(self):
		super().validate()
		self.add_model_value('fk_user', self.request().user)
		return self.valid()


	def commit(self):
		if Business.remove(self.model_values()):
			return True
		else:
			self.set_error('id', 'Failed to delete Bunisess!!')
		return False



business_address_fields = {
	'B_id':{'name': 'fk_business', 'validator': NoValidator},
	'A_id':{'name': 'fk_address', 'validator': NoValidator},
	'business_id':{'name': 'fk_business', 'validator': NoValidator},
	'address_id':{'name': 'fk_address', 'validator': NoValidator},
}

class BALinkForm(CreateForm):
	def __init__(self):
		super().__init__()
		self.m_fields = business_address_fields


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid

		return self.valid()


	def save(self):
		print('saving ....')
		print(self.model_values())
		return Business.create(self.model_values())



class BAUnLinkForm(CreateForm):
	def __init__(self):
		super().__init__()
		self.m_fields = business_address_fields


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid

		return self.valid()


	def delete(self):
		print('saving ....')
		print(self.model_values())
		return Business.remove(self.model_values())
