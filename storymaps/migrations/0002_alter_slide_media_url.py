# Generated by Django 3.2.1 on 2022-03-29 09:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storymaps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='slide',
            name='media_url',
            field=models.URLField(blank=True, max_length=400, null=True),
        ),
    ]
