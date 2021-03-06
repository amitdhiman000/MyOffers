# Generated by Django 2.1.7 on 2019-07-21 19:29

from django.db import migrations, models
import django.db.models.deletion
import mail.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PrivateMessageModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(default='<No subject>', max_length=200)),
                ('text', models.TextField()),
                ('fk_receiver', models.ForeignKey(default=mail.models.get_admin, on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_receiver', to='user.UserModel')),
                ('fk_sender', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fk_sender', to='user.UserModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PublicMessageModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('title', models.CharField(default='<No subject>', max_length=200)),
                ('text', models.TextField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
