from background_task import background
from upload.models import FileUpload
from user.models import User
from base.forms import *
## debug
import logging

## run after 60 seconds
@background(schedule=1*60)
def clear_file_upload(user_id, upload_id):
	print('clear_file_upload :: start')
	user = User.fetch_by_id(user_id)
	FileUpload.remove(upload_id, user)
	print('clear_file_upload :: done')
	#user.email_user('Here is a notification', 'You have been notified')



class FileUploadForm(CreateForm):

	def __init__(self):
		super().__init__()
		self.m_fields = {
			'image': {'name':'file', 'validator': None },
		}


	def parse(self, request, is_json):
		self.m_request = request
		if is_json == True:
			self.m_values = json.loads(request.body.decode('utf-8'))
		else:
			self.m_values = request.FILES

		for key in self.m_values:
			if key in self.m_fields:
				self.make_model_value(key, self.m_values[key])
		return True


	def clean(self):
		return True


	def validate(self):
		super().validate()
		self.add_model_value('fk_user', self.request().user)
		return self.valid()


	def commit(self):
		print(self.model_values())
		upload = FileUpload.create(self.model_values())
		if upload != None:
			pass
			#clear_file_upload(self.m_user.id, upload.id)
		else:
			self.m_errors['upload'] = 'File save server error, try again'
		return upload
