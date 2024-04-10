# Generated by Django 3.2.1 on 2024-02-13 12:31

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0002_auto_20240212_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='routesection',
            name='elr_fk',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.elr'),
        ),
        migrations.AddField(
            model_name='routesection',
            name='geodata',
            field=models.JSONField(blank=True, default=None, null=True),
        ),
        migrations.AddField(
            model_name='routesection',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
