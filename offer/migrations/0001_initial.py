# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-03-13 15:17
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc
import django.utils.timezone
import offer.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('business_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('business_name', models.CharField(max_length=30)),
                ('business_desc', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'business',
                'verbose_name_plural': 'business',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_name', models.CharField(max_length=30)),
                ('product_image', models.FileField(upload_to=offer.models.user_product_dir)),
                ('discount', models.CharField(max_length=3)),
                ('create_time', models.DateTimeField(default=django.utils.timezone.now)),
                ('start_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_date', models.DateTimeField(default=datetime.datetime(2017, 3, 18, 15, 17, 27, 259687, tzinfo=utc))),
                ('description', models.TextField()),
                ('fk_area', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Area')),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User')),
            ],
            options={
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
            },
        ),
    ]
