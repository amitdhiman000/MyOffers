# Generated by Django 2.0 on 2017-12-20 18:45

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('phone', models.CharField(blank=True, max_length=10)),
                ('address', models.CharField(max_length=50)),
                ('landmark', models.CharField(blank=True, max_length=50)),
                ('latitude', models.CharField(blank=True, max_length=10)),
                ('longitude', models.CharField(blank=True, max_length=10)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('flags', models.CharField(default='', max_length=10)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Area',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('pincode', models.CharField(blank=True, max_length=10)),
            ],
            options={
                'verbose_name': 'area',
                'verbose_name_plural': 'areas',
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'city',
                'verbose_name_plural': 'cities',
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name': 'country',
                'verbose_name_plural': 'countries',
            },
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('latitude', models.CharField(max_length=10)),
                ('longitude', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('fk_country', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.Country')),
            ],
            options={
                'verbose_name': 'state',
                'verbose_name_plural': 'states',
            },
        ),
        migrations.AddField(
            model_name='city',
            name='fk_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.Country'),
        ),
        migrations.AddField(
            model_name='city',
            name='fk_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.State'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_city',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.City'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_country',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.Country'),
        ),
        migrations.AddField(
            model_name='area',
            name='fk_state',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.State'),
        ),
        migrations.AddField(
            model_name='address',
            name='fk_area',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locus.Area'),
        ),
        migrations.AddField(
            model_name='address',
            name='fk_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.User'),
        ),
    ]
