# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-05-21 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('public', '0003_auto_20170423_1900'),
    ]

    operations = [
        migrations.AddField(
            model_name='guestmessage',
            name='title',
            field=models.CharField(default='blank', max_length=200),
        ),
        migrations.AddField(
            model_name='usermessage',
            name='title',
            field=models.CharField(default='blank', max_length=200),
        ),
    ]
