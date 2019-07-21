from background_task import background
from upload.models import FileUploadModel
from user.models import UserModel
from base.controls import BaseControl


## run after 60 seconds
@background(schedule=1*60)
def clear_file_upload(user_id, upload_id):
	print('clear_file_upload :: start')
	user = User.fetch_by_id(user_id)
	FileUploadModel.remove(upload_id, user)
	print('clear_file_upload :: done')
	#user.email_user('Here is a notification', 'You have been notified')



class FileUploadControl(BaseControl):
	def parseRequest(self, request):
		self.m_file = None
		self.m_user = request.user
		if request.FILES is None:
			self.m_errors['upload'] = 'No file attached'
			self.m_valid = False
			return False
		else:
			for key in request.FILES:
				self.m_file = request.FILES[key]
				break
			pprint('file : '+self.m_file.name)
		return True


	def validate(self):
		if self.m_valid is False:
			return self.m_valid

		print('validating')
		valid = True

		user = User.fetch_user(self.m_user)
		if user is not None:
			self.m_user = user
		else:
			self.m_errors['upload'] = 'Invalid user'
			valid = False

		self.m_valid = valid
		return self.m_valid


	def execute(self):
		if self.m_valid is False:
			return None

		upload = FileUpload.create(self.m_file, self.m_user)
		if upload is not None:
			pass
			#clear_file_upload(self.m_user.id, upload.id)
		else:
			self.m_errors['upload'] = 'File upload server error, try again'
		return upload
