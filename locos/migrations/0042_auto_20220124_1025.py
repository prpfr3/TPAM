# Generated by Django 3.2.1 on 2022-01-24 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0041_auto_20220123_1309'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lococlass',
            old_name='numbers_rebuilt',
            new_name='number_rebuilt',
        ),
        migrations.AddField(
            model_name='lococlass',
            name='alternator',
            field=models.CharField(blank=True, default='', max_length=40),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='axle_load_class',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='bogie',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='bogies',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='brakeforce',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='coolant_capacity',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='couplers',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='current_pickups',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='displacement',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='electric_systems',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='engine_maximum_rpm',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='engine_type',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='gear_ratio',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='generator',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='height_pantograph',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='lubricant_capacity',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='model',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='mu_working',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='pivot_centres',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='power_output',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='power_output_continuous',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='power_output_one_hour',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='power_output_starting',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='prime_mover',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='rpm_range',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='safety_systems',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='traction_motors',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='transmission',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='wheel_configuration_aar',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='wheel_configuration_commonwealth',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
        migrations.AddField(
            model_name='lococlass',
            name='wheel_diameter',
            field=models.CharField(blank=True, default='', max_length=200),
        ),
    ]