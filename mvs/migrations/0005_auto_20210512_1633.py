# Generated by Django 3.2.1 on 2021-05-12 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mvs', '0004_delete_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heritagesite',
            name='notes',
            field=models.TextField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='heritagesite',
            name='url',
            field=models.URLField(default=None, null=True),
        ),
        migrations.AlterField(
            model_name='heritagesite',
            name='wikislug',
            field=models.SlugField(default=None, max_length=255, null=True),
        ),
    ]
