# Generated by Django 3.2.1 on 2023-07-29 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('timelines', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timelineslide',
            name='media_caption',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='timelineslide',
            name='media_credit',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AlterField(
            model_name='timelineslide',
            name='media_url',
            field=models.URLField(blank=True, default='', max_length=400),
        ),
    ]
