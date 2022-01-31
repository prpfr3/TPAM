# Generated by Django 3.2.1 on 2022-01-04 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0008_company'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, null=True)),
            ],
            options={
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='CompanyCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locos.category')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locos.company')),
            ],
        ),
    ]
