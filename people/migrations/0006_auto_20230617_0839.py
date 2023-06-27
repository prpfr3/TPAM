# Generated by Django 3.2.1 on 2023-06-17 07:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0005_person_references'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='person',
            options={'ordering': ('name',), 'verbose_name_plural': 'People'},
        ),
        migrations.AlterField(
            model_name='person',
            name='source',
            field=models.IntegerField(choices=[(1, 'Wikipedia'), (2, 'Custom'), (3, 'South Western Railway Magazine')], default=1),
        ),
    ]
