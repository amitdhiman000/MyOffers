from base.forms import *
from base.validators import *
from business.validators import *
from business.models import (Business, Category)


model_fields = [
	{'name': 'id', 'validator': NoValidator},
	{'name': 'name', 'validator': BusinessNameValidator},
	{'name': 'about', 'validator': DescriptionValidator},
	{'name': 'website', 'validator': WebsiteValidator},
	{'name': 'fk_category', 'validator': BusinessCategoryValidator},
]

form_fields = {
	## for html form
	'B_id': model_fields[0],
	'B_name': model_fields[1],
	'B_about': model_fields[2],
	'B_website': model_fields[3],
	'B_category': model_fields[4],
	## for json
	'id': model_fields[0],
	'name': model_fields[1],
	'about': model_fields[2],
	'website': model_fields[3],
	'category': model_fields[4],
}


class BusinessRegForm(CreateForm):

	def __init__(self):
		super().__init__()
		self.m_fields = form_fields


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid

		cat = Category.fetch_by_id(self.model_values()['fk_category'])
		if cat != None:
			self.add_model_value('fk_category', cat)
		else:
			self.set_error('fk_category', 'Category not found')
			return False
		self.add_model_value('fk_user', self.m_request.user)
		return True


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



class BusinessDeleteForm(Form):

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
			return False
		else:
			self.set_error('id', 'Failed to delete Bunisess!!')
		return True
