# Generated by Django 3.2.1 on 2022-01-21 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0033_classowneroperator'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='loco_classes',
            field=models.ManyToManyField(to='locos.LocoClass'),
        ),
    ]