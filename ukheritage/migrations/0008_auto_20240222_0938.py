# Generated by Django 3.2.1 on 2024-02-22 09:38

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ukheritage', '0007_alter_gdukparksgardens_capturesca'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gdukworldheritagesites',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
        migrations.AlterField(
            model_name='myplaces',
            name='geometry',
            field=django.contrib.gis.db.models.fields.GeometryField(blank=True, null=True, srid=4326),
        ),
    ]
