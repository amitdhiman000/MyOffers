# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-04-23 19:00
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0004_auto_20170423_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='expire_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 4, 28, 19, 0, 9, 299052, tzinfo=utc)),
        ),
    ]