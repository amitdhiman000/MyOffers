# Generated by Django 2.1.7 on 2019-07-21 19:29

import base.apputil
import datetime
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('locus', '0001_initial'),
        ('business', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OfferAddressMapModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fk_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.AddressModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfferCategoryMapModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('fk_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.CategoryModel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OfferModel',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('slug', models.SlugField(unique=True)),
                ('name', models.CharField(max_length=30)),
                ('details', models.TextField()),
                ('image', models.FileField(upload_to=base.apputil.App_UserFilesDir)),
                ('price', models.IntegerField(default=100)),
                ('discount', models.IntegerField(default=0)),
                ('discount_price', models.IntegerField(default=100)),
                ('start_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('expire_at', models.DateTimeField(default=datetime.datetime(2019, 7, 26, 19, 29, 49, 921797, tzinfo=utc))),
                ('fk_business', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='business.BusinessModel')),
                ('fk_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.UserModel')),
            ],
            options={
                'verbose_name': 'offer',
                'verbose_name_plural': 'offers',
            },
        ),
        migrations.AddField(
            model_name='offercategorymapmodel',
            name='fk_offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.OfferModel'),
        ),
        migrations.AddField(
            model_name='offeraddressmapmodel',
            name='fk_offer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='offer.OfferModel'),
        ),
    ]
