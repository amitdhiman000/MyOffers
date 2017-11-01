from django.conf import settings
from django.db import models
from django.utils import timezone

from user.models import User
from common.apputil import App_UserFilesDir
## debug
import traceback
from pprint import pprint

class FileUpload(models.Model):
	id = models.BigAutoField(primary_key=True)
	file = models.FileField(upload_to=App_UserFilesDir)
	used = models.IntegerField(default=0)
	created = models.DateTimeField(default=timezone.now)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)

	@classmethod
	def create(klass, file_data, user):
		obj = klass(file=file_data, fk_user=user)
		obj.save()
		return obj

	@classmethod
	def remove(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			if obj.used == 0:
				# delete the file from disk
				obj.file.delete()
			obj.delete()
			return True
		except:
			print('Failed to delete file')
			traceback.print_exc()
			return False

	@classmethod
	def fetch_file(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			return obj
		except:
			print('Failed to get file name')
			traceback.print_exc()
			return None

	@classmethod
	def mark_used(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			obj.used = 1
			obj.save()
			return True
		except:
			print('Failed to mark as used')
			traceback.print_exc()
			return False
