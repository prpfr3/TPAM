# Generated by Django 3.2.1 on 2023-05-07 11:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0013_route_elrs'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'managed': False},
        ),
        migrations.AlterModelOptions(
            name='routegeoclosed',
            options={'managed': False, 'verbose_name': 'Closed Route Geometries', 'verbose_name_plural': 'Closed Routes Geometries'},
        ),
    ]
