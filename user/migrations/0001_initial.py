# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-09-03 17:24
from __future__ import unicode_literals

import apputil
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locus', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('line1', models.CharField(blank=True, max_length=50)),
                ('line2', models.CharField(blank=True, max_length=50)),
                ('geo_long', models.CharField(blank=True, max_length=10)),
                ('geo_lat', models.CharField(blank=True, max_length=10)),
                ('fk_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.Area')),
            ],
        ),
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
                ('image', models.FileField(default='/images/icons-svg/user.svg', upload_to=apputil.App_UserFilesDir)),
            ],
        ),
        migrations.AddField(
            model_name='address',
            name='fk_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
