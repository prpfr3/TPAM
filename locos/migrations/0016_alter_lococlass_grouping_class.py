# Generated by Django 3.2.1 on 2022-01-08 14:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0015_alter_lococlass_grouping_class'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lococlass',
            name='grouping_class',
            field=models.CharField(blank=True, default='', max_length=500),
        ),
    ]