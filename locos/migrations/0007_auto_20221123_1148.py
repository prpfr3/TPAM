# Generated by Django 3.2.1 on 2022-11-23 11:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0011_locationevent_elr_fk'),
        ('locos', '0006_rename_sighting_reference'),
    ]

    operations = [
        migrations.AddField(
            model_name='reference',
            name='ELR_fk',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='locations.elr'),
        ),
        migrations.AddField(
            model_name='reference',
            name='company_fk',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='locos.company'),
        ),
    ]
