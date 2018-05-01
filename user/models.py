from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.core.mail import send_mail
from base.apputil import App_UserFilesDir

import logging


class User(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50, blank=False, default='')
    email = models.EmailField()
    password = models.CharField(max_length=32, blank=False, default='')
    created_at = models.DateTimeField(default=timezone.now)
    phone = models.CharField(max_length=10, blank=True)
    # {-2: delete, -1:blocked, 0:inactive, 1:active }
    status = models.IntegerField(default=1)
    # {0:guest, 1:normal, 2:morderator, 3:author, 9:admin}
    level = models.IntegerField(default=1)
    # profile image by default : user.svg
    image = models.FileField(upload_to=App_UserFilesDir, default=settings.DEFAULT_USER_IMAGE)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def url(self):
        return '/user/%s/' % self.email

    @classmethod
    def queryset(klass):
        fields = ('id', 'name', 'email', 'phone')
        return klass.objects.values(*fields)

    @classmethod
    def create(klass, values):
        try:
            return klass.objects.create(level=9, **values)
        except Exception as ex:
            logging.error(ex)
        return None

    @classmethod
    def update(klass, values):
        try:
            user_id = values['id']
            return klass.objects.filter(id=user_id).update(**values)
        except Exception as ex:
            logging.error(ex)
        return None

    @classmethod
    def fetch_all(klass):
        return klass.queryset().all()

    @classmethod
    def fetch_user(klass, user):
        try:
            return klass.objects.get(email=user.email)
        except Exception as ex:
            logging.error(ex)
        return None

    @classmethod
    def fetch_by_id(klass, id):
        try:
            return klass.objects.get(id=id)
        except Exception as ex:
            logging.error(ex)
        return None

    @classmethod
    def update_name(klass, name, user):
        u = klass.fetch_user(user)
        u.name = name
        u.save()
        return u.name

    @classmethod
    def update_email(klass, email, user):
        u = klass.fetch_user(user)
        u.email = email
        u.save()
        return u.email

    @classmethod
    def update_phone(klass, phone, user):
        u = klass.fetch_user(user)
        u.phone = phone
        u.save()
        return u.phone

    @classmethod
    def update_password(klass, password, user):
        u = klass.fetch_user(user)
        u.password = password
        u.save()
        return 'xxxxxxxx'

    @classmethod
    def check_password(klass, password, user):
        u = klass.fetch_user(user)
        return u.password == password

    @classmethod
    def check_email(klass, email):
        return klass.objects.filter(email=email).exists()

    @classmethod
    def check_creds(klass, email, password):
        try:
            return klass.objects.get(email=email, password=password)
            # return klass.objects.filter(email=email, password=password).first()
        except Exception as ex:
            logging.error(ex)
        return None

    # Always return True, user object is created means loggedin.
    def is_loggedin(self):
        return True

    def email_user(self, from_email=None, subject='Hello', message=None):
        send_mail(subject, message, from_email, self.email)


class Guest(object):

    def __init__(self):
        self.id = -1
        self.name = 'Guest'
        self.email = 'guest@email.com'

    def fetch_name(self):
        return self.name

    def is_loggedin(self):
        return False
