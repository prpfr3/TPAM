# Generated by Django 3.2.1 on 2023-01-24 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0012_auto_20230124_1554'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='date',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='date_datetime',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reference',
            name='lococlass',
            field=models.ManyToManyField(blank='True', through='locos.LocoClassSighting', to='locos.LocoClass'),
        ),
    ]
