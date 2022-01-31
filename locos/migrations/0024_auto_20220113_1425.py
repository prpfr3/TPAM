# Generated by Django 3.2.1 on 2022-01-13 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0023_auto_20220113_1016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lococlass',
            name='cylinder_size',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='lococlass',
            name='firegrate_area',
            field=models.CharField(blank=True, default='', max_length=75),
        ),
        migrations.AlterField(
            model_name='lococlass',
            name='gauge',
            field=models.CharField(blank=True, default='', max_length=80),
        ),
        migrations.AlterField(
            model_name='lococlass',
            name='loco_weight',
            field=models.CharField(blank=True, default='', max_length=250),
        ),
        migrations.AlterField(
            model_name='lococlass',
            name='numbers',
            field=models.CharField(blank=True, default='', max_length=700),
        ),
    ]
