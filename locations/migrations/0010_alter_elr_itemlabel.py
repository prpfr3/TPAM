# Generated by Django 3.2.1 on 2022-11-19 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0009_auto_20221119_0946'),
    ]

    operations = [
        migrations.AlterField(
            model_name='elr',
            name='itemLabel',
            field=models.CharField(blank=True, default='', max_length=400),
        ),
    ]