# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-12-15 04:15
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('address_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('house_info', models.CharField(blank=True, max_length=50)),
                ('geo_long', models.CharField(blank=True, max_length=10)),
                ('geo_lat', models.CharField(blank=True, max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('area_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('area_name', models.CharField(blank=True, max_length=50)),
                ('area_pin', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
            },
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved', models.BooleanField(default=False)),
                ('title', models.CharField(max_length=100)),
                ('sub_title', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved', models.BooleanField(default=False)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Article')),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ArticleReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.IntegerField(default=1)),
                ('article', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Article')),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('city_name', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='CommentReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.IntegerField(default=1)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.ArticleComment')),
            ],
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('country_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('country_name', models.CharField(blank=True, max_length=50)),
            ],
            options={
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='ReplyComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField()),
                ('created_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('edited_date', models.DateTimeField(default=django.utils.timezone.now)),
                ('approved', models.BooleanField(default=False)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'posts',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReplyCommentReaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reaction', models.IntegerField(default=1)),
                ('comment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.ReplyComment')),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('state_id', models.IntegerField(primary_key=True, serialize=False, unique=True)),
                ('state_name', models.CharField(blank=True, max_length=50)),
                ('fk_country_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Country')),
            ],
            options={
                'verbose_name': 'state',
                'verbose_name_plural': 'states',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name', models.CharField(max_length=50)),
                ('topic_desc', models.CharField(blank=True, max_length=100)),
                ('topic_followers', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TopicFollower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Topic')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('password', models.CharField(default='', max_length=32)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('status', models.IntegerField(default=1)),
                ('level', models.IntegerField(default=1)),
            ],
        ),
        migrations.AddField(
            model_name='topicfollower',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='topic',
            name='topic_author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='replycommentreaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='replycomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='replycomment',
            name='comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.ReplyComment'),
        ),
        migrations.AddField(
            model_name='commentreaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='city',
            name='fk_country_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Country'),
        ),
        migrations.AddField(
            model_name='city',
            name='fk_state_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.State'),
        ),
        migrations.AddField(
            model_name='articlereaction',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='articlecomment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_city_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.City'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_country_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Country'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_state_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.State'),
        ),
        migrations.AddField(
            model_name='address',
            name='fk_area_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.Area'),
        ),
    ]