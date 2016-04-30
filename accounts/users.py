from django.db import models

class User(models.Model):
	username = models.TextField(max_length=32)
	password = models.TextField(max_length=32)
	email = models.TextField(max_length=254)
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):              # __unicode__ on Python 2
        return self.username

	def save(self):
		try:
			super(self.__class__, self).save(*args, **kwargs)
			return True
		except:
			return False



class Consumer(User):


class Vendor(User):
	