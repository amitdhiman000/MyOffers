# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-28 15:23
from __future__ import unicode_literals

import apputil
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(default='', max_length=32)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('status', models.IntegerField(default=1)),
                ('level', models.IntegerField(default=1)),
                ('image', models.FileField(default='default/user.svg', upload_to=apputil.App_UserFilesDir)),
            ],
        ),
    ]
