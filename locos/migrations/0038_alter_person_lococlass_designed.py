# Generated by Django 3.2.1 on 2022-01-23 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0037_auto_20220123_1147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='lococlass_designed',
            field=models.ManyToManyField(through='locos.ClassDesigner', to='locos.LocoClass'),
        ),
    ]