from django.db import models
from base.models import CRUDModel
from datetime import (date, timedelta)
from user.models import User
import logging
# Create your models here.


class Message(CRUDModel):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=10, blank=True)
    title = models.CharField(max_length=200, default="blank")
    text = models.TextField()
    fk_user = models.ForeignKey(User, on_delete=models.CASCADE, default=None, null=True)

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
