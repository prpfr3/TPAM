# Generated by Django 3.2.1 on 2022-01-15 12:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0026_auto_20220115_1234'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='url',
        ),
    ]