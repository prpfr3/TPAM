# Generated by Django 3.2.1 on 2024-02-16 15:05

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ukheritage', '0004_alter_gdukscheduledmonuments_capturesca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gdukscheduledmonuments',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
