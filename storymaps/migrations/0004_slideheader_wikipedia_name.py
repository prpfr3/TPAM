# Generated by Django 3.2.7 on 2022-09-27 11:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('storymaps', '0003_slide_wikipedia_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='slideheader',
            name='wikipedia_name',
            field=models.CharField(blank=True, default='', max_length=1000),
        ),
    ]