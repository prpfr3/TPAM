# Generated by Django 3.2.1 on 2022-01-16 14:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0029_person_birthplace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sighting',
            name='geometry',
        ),
    ]
