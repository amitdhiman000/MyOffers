from django.db import models
from base.models import CRUDModel
from datetime import (date, timedelta)
from user.models import User
import logging
# Create your models here.


def get_admin():
    return User.fetch_admin()


class PrivateMessage(CRUDModel):
    title = models.CharField(max_length=200, default="<No subject>")
    text = models.TextField()
    fk_sender = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name='fk_sender')
    fk_receiver = models.ForeignKey(User, on_delete=models.DO_NOTHING, default=get_admin, related_name='fk_receiver')

    @classmethod
    def fetch_latest(klass):
        return klass.objects.latest('created_at')

    @classmethod
    def fetch_by_date(klass, start, end):
        startdate = date.today()
        enddate = startdate + timedelta(days=6)
        return klass.objects.filter(created_at_range=[startdate, enddate])

    @classmethod
    def fetch_by_index(klass, start, end):
        return []


class PublicMessage(CRUDModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=200, default="<No subject>")
    text = models.TextField()

    @classmethod
    def fetch_latest(klass):
        return klass.objects.latest('created_at')

    @classmethod
    def fetch_by_date(klass, start, end):
        startdate = date.today()
        enddate = startdate + timedelta(days=6)
        return klass.objects.filter(created_at_range=[startdate, enddate])

    @classmethod
    def fetch_by_index(klass, start, end):
        return []