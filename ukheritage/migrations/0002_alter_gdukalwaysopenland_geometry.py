# Generated by Django 3.2.1 on 2024-02-16 14:44

# import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("ukheritage", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="gdukalwaysopenland",
            name="geometry",
            field=models.TextField(blank=True, null=True),
        ),
    ]
