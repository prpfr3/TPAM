# Generated by Django 3.2.1 on 2022-01-24 10:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0042_auto_20220124_1025'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lococlass',
            name='alternator',
            field=models.CharField(blank=True, default='', max_length=75),
        ),
        migrations.AlterField(
            model_name='lococlass',
            name='generator',
            field=models.CharField(blank=True, default='', max_length=150),
        ),
    ]