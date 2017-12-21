from django.db import models
import logging


class BaseModel(models.Model):
	id = models.BigAutoField(primary_key=True)

	class Meta:
		abstract = True


	def url(self):
		return "/{0}/{1}/{1}/".format(self.__module__, self.__class__.__name__, self.id)
		#return '/locus/address/'+ str(self.id) + '/'


	@classmethod
	def create(klass, values):
		try:
			obj = klass.objects.get_or_create(**values)[0]
			return obj
		except Exception as e:
			logging.error(e)
		return None


	@classmethod
	def update(klass, values):
		try:
			id_ = values['id']
			obj = klass.objects.filter(id=id_).update(**values)
			return obj
		except Exception as ex:
			logging.error(ex)
		return None


	@classmethod
	def remove(klass, values):
		try:
			obj = klass.objects.filter(**values)
			if obj.exists():
				obj.delete()
				return True
		except Exception as ex:
			logging.error(ex)
		return False


	@classmethod
	def fetch(klass, filters, start=0, count=10):
		try:
			return klass.objects.filter(**filters)[:start:(start+count)]
		except Exception as e:
			logging.error(e)
		return None
