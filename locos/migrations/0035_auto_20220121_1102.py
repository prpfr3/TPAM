# Generated by Django 3.2.1 on 2022-01-21 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0034_company_loco_classes'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companycategory',
            options={'managed': True},
        ),
        migrations.RemoveField(
            model_name='companycategory',
            name='company',
        ),
        migrations.AddField(
            model_name='company',
            name='company_categories',
            field=models.ManyToManyField(to='locos.CompanyCategory'),
        ),
        migrations.AlterField(
            model_name='companycategory',
            name='category',
            field=models.CharField(max_length=100, null=True),
        ),
    ]