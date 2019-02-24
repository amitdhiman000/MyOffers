from django.db import models
import logging


class CRUDQueryset(models.query.QuerySet):
	def withurl(self):
		print('This is called from custom query set')
		for item in self:
			item.url = item.url()
			print(item.url)
		return self



class CRUDManager(models.Manager):
	def get_queryset(self):
		return CRUDQueryset(self.model, using=self._db)

	def withurl(self):
		return self.get_queryset().withurl()



class CRUDModel(models.Model):
	id = models.BigAutoField(primary_key=True)

	objects = CRUDManager()

	'''
	def __init__(self, *args, **kwargs):
		print('Called init')
		super().__init__(self, *args, **kwargs)
		self.url = self.url()
	'''

	class Meta:
		abstract = True


	def url(self):
		## class name to lower
		class_name = self.__class__.__name__.lower()
		## remove ".models" from module name
		module_name = self.__class__.__module__[:-7]
		if module_name == class_name:
			return "/{0}/{1}/".format(class_name, self.id)
			#return '/locus/' + (self.id)+ '/'
		else:
			return "/{0}/{1}/{2}/".format(module_name, class_name, self.id)
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
