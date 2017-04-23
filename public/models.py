from django.conf import settings
from django.db import models
from django.utils import timezone
from user.models import User

import traceback
# Create your models here.

class UserMessage(models.Model):
	id = models.BigAutoField(primary_key=True)
	text = models.TextField()
	created = models.DateTimeField(default=timezone.now)
	fk_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)

	@classmethod
	def create(klass, msg):
		msg.save()
		return msg

	def remove(klass, id):
		try:
			klass.objects.delete(id=id)
		except:
			print('Failed to delete the message')
			traceback.print_exc()

	@classmethod
	def get_latest_messages(klass):
		return klass.objects.filter(create_is_between);
	
	@classmethod
	def get_all_messages(klass):
		return klass.objects.all();

	@classmethod
	def get_by_date(klass, start, end):
		startdate = date.today()
		enddate = startdate + timedelta(days=6)
		return klass.objects.filter(created_range(startdate, enddate))

	@classmethod
	def get_by_index(klass, start, end):
		return [];

	@classmethod
	def get_by_email(klass):
		return [];


class GuestMessage(models.Model):
	id = models.BigAutoField(primary_key=True)
	name = models.CharField(max_length=50)
	email = models.EmailField()
	phone = models.CharField(max_length=10, blank=True)
	text = models.TextField()
	created = models.DateTimeField(default=timezone.now)


	@classmethod
	def create(klass, msg):
		msg.save()
		return msg

	def remove(klass, id):
		try:
			klass.objects.delete(id=id)
		except:
			print('Failed to delete the message')
			traceback.print_exc()

	@classmethod
	def get_latest_messages(klass):
		return klass.objects.filter(create_is_between);
	
	@classmethod
	def get_all_messages(klass):
		return klass.objects.all();

	@classmethod
	def get_by_date(klass, start, end):
		startdate = date.today()
		enddate = startdate + timedelta(days=6)
		return klass.objects.filter(created_range(startdate, enddate))

	@classmethod
	def get_by_index(klass, start, end):
		return [];

	@classmethod
	def get_by_email(klass):
		return [];