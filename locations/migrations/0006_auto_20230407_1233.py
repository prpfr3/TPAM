# Generated by Django 3.2.1 on 2023-04-07 11:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0005_auto_20230406_1608'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='location',
            options={'managed': True},
        ),
        migrations.CreateModel(
            name='ELRLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('elr_fk', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.CASCADE, to='locations.elr')),
                ('location_fk', models.ForeignKey(
                    on_delete=django.db.models.deletion.CASCADE, to='locations.location')),
            ],
        ),
    ]
