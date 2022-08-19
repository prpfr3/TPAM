# Generated by Django 3.2.1 on 2022-08-15 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0086_auto_20220815_1608'),
    ]

    operations = [
        migrations.RenameField(
            model_name='locomotive',
            old_name='brd_withdrawn_date',
            new_name='brd_withdrawn_date_recorded',
        ),
        migrations.AddField(
            model_name='locomotive',
            name='brd_withdrawn_date_datetime',
            field=models.DateField(blank=True, null=True),
        ),
    ]
