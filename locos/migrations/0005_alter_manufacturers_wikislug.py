# Generated by Django 3.2.1 on 2022-01-04 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0004_alter_manufacturers_manufacturer_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturers',
            name='wikislug',
            field=models.SlugField(default=None, max_length=200),
        ),
    ]
