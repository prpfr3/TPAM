# Generated by Django 3.2.1 on 2022-01-18 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0031_auto_20220118_1051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='person',
            old_name='died',
            new_name='diedplace',
        ),
        migrations.AddField(
            model_name='person',
            name='dieddate',
            field=models.CharField(blank=True, default='', max_length=10),
        ),
    ]