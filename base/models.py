from django.db import models
import logging


class CRUDModel(models.Model):
	id = models.BigAutoField(primary_key=True)

	class Meta:
		abstract = True


	def url(self):
		if self.__module__ == self.__class__.__name__:
			return "/{0}/{1}/".format(self.__module__, self.id)
			#return '/locus/' + (self.id)+ '/'
		else:
			return "/{0}/{1}/{1}/".format(self.__module__, self.__class__.__name__, self.id)
			#return '/locus/address/'+ str(self.id) + '/'


	@classmethod
	def create(klass, values):
		try:
			obj = klass.objects.get_or_create(**values)[0]
			return obj
		except Exception as ex:
			logging.error(ex)
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
	def fetch(klass, filters, start=0, count=0):
		try:
			if count > 0:
				return klass.objects.filter(**filters)[:start:(start+count)]
			else:
				return klass.objects.filter(**filters)
		except Exception as ex:
			logging.error(ex)
		return None


	@classmethod
	def fetch_all(klass):
		return klass.objects.all()


	@classmethod
	def fetch_by_id(klass, id_):
		return klass.objects.filter(id=id_).first()