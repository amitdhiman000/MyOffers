# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-08-15 18:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GuestMessage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('title', models.CharField(default='blank', max_length=200)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='UserMessage',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(default='blank', max_length=200)),
                ('text', models.TextField()),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
    ]
