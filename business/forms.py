from common.forms import *
from common.validators import *
from user.models import User
from user import backends


model_fields = [
	{'name': 'id', 'validator': NoValidator},
	{'name': 'name', 'validator': BusinessNameValidator},
	{'name': 'about', 'validator': DesctiptionValidator},
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
		return True


	def save(self):
		print('saving ....')
		return User.create(self.values())



class BusinessUpdateForm(UpdateForm):

	def __init__(self):
		super().__init__()
		self.m_form_fields = form_fields
		self.m_model_fields = model_fields


	def validate(self):
		is_valid = super().validate()
		if not is_valid:
			return is_valid
		self.set_value('id', self.m_request.user.id)
		print(self.m_values)
		return True


	def update(self):
		print('saving ....')
		if User.update(self.values()):
			return self.result()
		else:
			return None



class BusinessDeleteForm(Form):

	def __init__(self):
		super().__init__()
		self.m_form_fields = {
			'U_id': 'id',
			'id': 'id'
		}
		self.m_model_fields = {
			'id': {'name':'id', 'validator':None},
		}

	def validate(self):
		return super().validate()


	def commit(self):
		business_id = self.m_values['id']
		if Business.remove(business_id):
			return False
		else:
			self.set_error('id', 'Failed to delete Bunisess!!')
		return True
