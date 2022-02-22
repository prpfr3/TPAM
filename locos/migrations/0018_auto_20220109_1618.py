# Generated by Django 3.2.1 on 2022-01-09 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0017_auto_20220108_1559'),
    ]

    operations = [
        migrations.AddField(
            model_name='lococlass',
            name='adhesion_factor',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='build_date',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='coupled_diameter',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='cylinder_size',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='cylinders',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='disposition',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='driver_diameter',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='firegrate_area',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='fuel_capacity',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='fuel_type',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
    ]