# Generated by Django 3.2.1 on 2022-01-08 14:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0014_lococlass_axle_load'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lococlass',
            name='grouping_class',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]
