# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-11-13 18:32
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('offer', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='expire_at',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 18, 18, 32, 14, 354084, tzinfo=utc)),
        ),
    ]
