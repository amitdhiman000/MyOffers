# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-23 18:06
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0002_auto_20170330_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 28, 18, 6, 56, 101281, tzinfo=utc)),
        ),
    ]