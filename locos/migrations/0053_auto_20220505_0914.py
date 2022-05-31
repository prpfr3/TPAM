# Generated by Django 3.2.1 on 2022-05-05 08:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0052_auto_20220505_0853'),
    ]

    operations = [
        migrations.AddField(
            model_name='sighting',
            name='short_description',
            field=models.CharField(blank='True', default=None, max_length=50, null='True'),
            preserve_default='True',
        ),
        migrations.AddField(
            model_name='sighting',
            name='url',
            field=models.URLField(blank=True, max_length=300, null=True),
        ),
    ]
