# Generated by Django 3.2.1 on 2024-02-22 09:38

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0004_auto_20240213_1451'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ukarea',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]