# Generated by Django 3.2.1 on 2022-11-21 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0003_delete_elr'),
    ]

    operations = [
        migrations.AddField(
            model_name='locomotive',
            name='number_as_built',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]