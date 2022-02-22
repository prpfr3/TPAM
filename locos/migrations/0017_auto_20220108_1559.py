# Generated by Django 3.2.1 on 2022-01-08 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0016_alter_lococlass_grouping_class'),
    ]

    operations = [
        migrations.AddField(
            model_name='lococlass',
            name='boiler',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='boiler_diameter',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='boiler_model',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='boiler_pitch',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='boiler_pressure',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='boiler_tube_plates',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]