# Generated by Django 3.2.1 on 2022-01-04 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0006_manufacturers_brsl_manufacturer_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufacturers',
            name='brsl_manufacturer_code',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]