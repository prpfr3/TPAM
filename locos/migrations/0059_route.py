# Generated by Django 3.2.1 on 2022-05-18 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0058_auto_20220508_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='Route',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=500)),
                ('wikislug', models.SlugField(default=None, max_length=255, null=True)),
            ],
        ),
    ]
