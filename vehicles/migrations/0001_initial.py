# Generated by Django 3.2.1 on 2021-06-20 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('maps', '0009_auto_20210514_1044'),
    ]

    operations = [
        migrations.CreateModel(
            name='VehicleMake',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=50)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name_plural': 'Vehicle Make',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VehicleModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model', models.CharField(max_length=80)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('make', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='vehicles.vehiclemake', verbose_name='Vehicle Make')),
            ],
            options={
                'verbose_name_plural': 'Vehicle Models',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VehicleType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=25, null=True)),
            ],
            options={
                'verbose_name_plural': 'Vehicle Types',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='VehicleVariant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('variant', models.CharField(max_length=80)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('model', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='vehicles.vehiclemodel', verbose_name='Vehicle Model')),
            ],
            options={
                'verbose_name_plural': 'Vehicle Variants',
                'managed': True,
            },
        ),
        migrations.AddField(
            model_name='vehiclemake',
            name='type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='vehicles.vehicletype', verbose_name='Vehicle Type'),
        ),
        migrations.CreateModel(
            name='VehicleImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(default=None, max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('notes', models.TextField(default=None)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='maps.heritagesite', verbose_name='Location')),
                ('make', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='vehicles.vehiclemake', verbose_name='Vehicle Make')),
                ('model', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='vehicles.vehiclemodel', verbose_name='Vehicle Model')),
                ('visit', models.ForeignKey(default=None, on_delete=django.db.models.deletion.SET_DEFAULT, to='maps.visit', verbose_name='Visit')),
            ],
        ),
        migrations.CreateModel(
            name='VehicleBMImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('url', models.URLField()),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/')),
                ('description', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rvimages_created', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, related_name='rvimages_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UKLicensedVehicles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('year_ending', models.PositiveIntegerField(default='2020')),
                ('year_licensed', models.CharField(default=None, max_length=10)),
                ('number_licensed', models.PositiveIntegerField(default=None)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('make', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='type', chained_model_field='type', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehiclemake')),
                ('model', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='make', chained_model_field='make', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehiclemodel')),
                ('type', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='vehicles.vehicletype', verbose_name='Vehicle Type')),
                ('variant', smart_selects.db_fields.ChainedForeignKey(auto_choose=True, chained_field='model', chained_model_field='model', default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='vehicles.vehiclevariant')),
            ],
            options={
                'verbose_name_plural': 'UK Licensed Vehicles',
                'managed': True,
            },
        ),
    ]
