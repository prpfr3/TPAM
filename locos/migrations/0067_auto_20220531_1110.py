# Generated by Django 3.2.1 on 2022-05-31 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0066_alter_routemap_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='routelocation',
            name='td1',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='routelocation',
            name='td2',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='routelocation',
            name='td3',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='routelocation',
            name='td4',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='routelocation',
            name='td5',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='routelocation',
            name='td6',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='routelocation',
            name='tr',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]