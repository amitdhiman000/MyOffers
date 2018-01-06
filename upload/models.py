from django.conf import settings
from django.db import models
from django.utils import timezone

from user.models import User
from base.apputil import App_UserFilePath
## debug
import logging


def file_upload_path(inst, filename):
	return App_UserFilePath(inst.fk_user, filename)


class FileUpload(models.Model):
	id = models.BigAutoField(primary_key=True)
	file = models.FileField(upload_to=file_upload_path)
	used = models.IntegerField(default=0)
	created_at = models.DateTimeField(default=timezone.now)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE)


	@classmethod
	def create(klass, values):
		obj = klass.objects.create(**values)
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
		except Exception as ex:
			logging.error(ex)
			return False


	@classmethod
	def fetch_file(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			return obj
		except Exception as ex:
			logging.error(ex)
			return None


	@classmethod
	def mark_used(klass, file_id, user):
		try:
			obj = klass.objects.get(id=file_id, fk_user=user)
			obj.used = 1
			obj.save()
			return True
		except Exception as ex:
			logging.error(ex)
			return False
