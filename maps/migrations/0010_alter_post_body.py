# Generated by Django 3.2.1 on 2023-01-24 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('maps', '0009_alter_post_body'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='body',
            field=models.TextField(),
        ),
    ]
