# Generated by Django 3.2.1 on 2022-12-30 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0014_location_elr_fk'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='osm_node',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='location',
            name='stationnamealt',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
