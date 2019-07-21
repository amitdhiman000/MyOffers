from django.conf import settings
from django.db import models
from base.models import (CRUDModel)

from base.apputil import (App_UserFilePath, App_TempFilePath)
## debug
import logging


def file_upload_path(inst, filename):
	return App_UserFilePath(inst.fk_user, filename)


def temp_upload_path(inst, filename):
	return App_TempFilePath(filename)

class FileUploadModel(CRUDModel):
	file = models.FileField(upload_to=temp_upload_path)
	used = models.IntegerField(default=0)
	#fk_user = models.ForeignKey(UserModel, on_delete=models.CASCADE)


	@classmethod
	def create(klass, values):
		obj = klass.objects.create(**values)
		return obj


	@classmethod
	def remove(klass, values):
		try:
			obj = klass.objects.get(**values)
			if obj.used == 0:
				# delete the file from disk
				obj.file.delete()
			obj.delete()
			return True
		except Exception as ex:
			logging.error(ex)
			return False


	@classmethod
	def fetch_file(klass, values):
		try:
			obj = klass.objects.get(**values)
			return obj
		except Exception as ex:
			logging.error(ex)
			return None


	@classmethod
	def mark_used(klass, **values):
		try:
			obj = klass.objects.get(**values)
			obj.used = 1
			obj.save()
			return True
		except Exception as ex:
			logging.error(ex)
			return False


class ImageUploadModel(CRUDModel):
	file = models.FileField(upload_to=temp_upload_path)
	used = models.IntegerField(default=0)

	@classmethod
	def create(klass, values):
		obj = klass.objects.create(**values)
		return obj

	@classmethod
	def remove(klass, values):
		try:
			obj = klass.objects.get(**values)
			if obj.used == 0:
				# delete the file from disk
				obj.file.delete()
			obj.delete()
			return True
		except Exception as ex:
			logging.error(ex)
			return False

	@classmethod
	def mark_used(klass, values):
		try:
			obj = klass.objects.get(**values)
			obj.used = 1
			obj.save()
			return True
		except Exception as ex:
			logging.error(ex)
			return False
