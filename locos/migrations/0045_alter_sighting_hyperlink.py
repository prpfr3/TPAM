# Generated by Django 3.2.1 on 2022-02-27 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0044_auto_20220204_1037'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sighting',
            name='hyperlink',
            field=models.CharField(blank=True, db_column='Hyperlink', max_length=300, null=True),
        ),
    ]
