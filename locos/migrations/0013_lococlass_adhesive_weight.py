# Generated by Django 3.2.1 on 2022-01-08 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0012_alter_company_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='lococlass',
            name='adhesive_weight',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]