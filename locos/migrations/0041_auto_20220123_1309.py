# Generated by Django 3.2.1 on 2022-01-23 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0040_rename_builder_name_builder_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='builder',
            name='lococlass_built',
            field=models.ManyToManyField(related_name='builder_builder', through='locos.ClassBuilder', to='locos.LocoClass'),
        ),
        migrations.AddField(
            model_name='company',
            name='lococlass_built',
            field=models.ManyToManyField(related_name='company_builder', through='locos.ClassBuilder', to='locos.LocoClass'),
        ),
        migrations.AddField(
            model_name='person',
            name='lococlass_built',
            field=models.ManyToManyField(related_name='person_builder', through='locos.ClassBuilder', to='locos.LocoClass'),
        ),
        migrations.AlterField(
            model_name='builder',
            name='lococlass_designed',
            field=models.ManyToManyField(related_name='builder_designer', through='locos.ClassDesigner', to='locos.LocoClass'),
        ),
        migrations.AlterField(
            model_name='person',
            name='lococlass_designed',
            field=models.ManyToManyField(related_name='person_designer', through='locos.ClassDesigner', to='locos.LocoClass'),
        ),
    ]
