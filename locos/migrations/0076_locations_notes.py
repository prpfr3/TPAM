# Generated by Django 3.2.1 on 2022-07-11 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0075_locations_opened'),
    ]

    operations = [
        migrations.AddField(
            model_name='locations',
            name='notes',
            field=models.TextField(blank=True, null=True),
        ),
    ]
