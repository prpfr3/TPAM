# Generated by Django 3.2.1 on 2023-03-23 11:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('notes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocoClass',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('wikiname', models.CharField(blank=True, default='', max_length=1000)),
                ('brdslug', models.CharField(blank=True,
                 default=None, max_length=255, null=True)),
                ('br_power_class', models.CharField(
                    blank=True, default='', max_length=5)),
                ('wheel_body_type', models.CharField(
                    blank=True, default='', max_length=100)),
                ('year_built', models.CharField(
                    blank=True, default='', max_length=100)),
                ('number_range', models.CharField(
                    blank=True, default='', max_length=100)),
                ('number_range_slug', models.SlugField(
                    blank=True, default=None, max_length=255, null=True)),
                ('year_first_built', models.CharField(
                    blank=True, default='', max_length=100)),
                ('year_last_built', models.CharField(
                    blank=True, default='', max_length=100)),
                ('number_built', models.CharField(
                    blank=True, default='', max_length=100)),
                ('img_slug', models.SlugField(blank=True,
                 default=None, max_length=255, null=True)),
                ('adhesive_weight', models.CharField(
                    blank=True, default='', max_length=200)),
                ('adhesion_factor', models.CharField(
                    blank=True, default='', max_length=40)),
                ('alternator', models.CharField(
                    blank=True, default='', max_length=75)),
                ('axle_load', models.CharField(
                    blank=True, default='', max_length=200)),
                ('axle_load_class', models.CharField(
                    blank=True, default='', max_length=200)),
                ('bogie', models.CharField(blank=True, default='', max_length=100)),
                ('bogies', models.CharField(blank=True, default='', max_length=100)),
                ('boiler', models.CharField(blank=True, default='', max_length=200)),
                ('boiler_pressure', models.CharField(
                    blank=True, default='', max_length=200)),
                ('boiler_diameter', models.CharField(
                    blank=True, default='', max_length=200)),
                ('boiler_model', models.CharField(
                    blank=True, default='', max_length=200)),
                ('boiler_pitch', models.CharField(
                    blank=True, default='', max_length=200)),
                ('boiler_tube_plates', models.CharField(
                    blank=True, default='', max_length=200)),
                ('brakeforce', models.CharField(
                    blank=True, default='', max_length=200)),
                ('build_date', models.CharField(
                    blank=True, default='', max_length=200)),
                ('coolant_capacity', models.CharField(
                    blank=True, default='', max_length=50)),
                ('couplers', models.CharField(blank=True, default='', max_length=50)),
                ('coupled_diameter', models.CharField(
                    blank=True, default='', max_length=50)),
                ('current_pickups', models.CharField(
                    blank=True, default='', max_length=300)),
                ('cylinder_size', models.CharField(
                    blank=True, default='', max_length=300)),
                ('cylinders', models.CharField(
                    blank=True, default='', max_length=125)),
                ('displacement', models.CharField(
                    blank=True, default='', max_length=200)),
                ('disposition', models.CharField(
                    blank=True, default='', max_length=200)),
                ('driver_diameter', models.CharField(
                    blank=True, default='', max_length=200)),
                ('electric_systems', models.CharField(
                    blank=True, default='', max_length=200)),
                ('engine_maximum_rpm', models.CharField(
                    blank=True, default='', max_length=50)),
                ('engine_type', models.CharField(
                    blank=True, default='', max_length=100)),
                ('firegrate_area', models.CharField(
                    blank=True, default='', max_length=100)),
                ('fuel_capacity', models.CharField(
                    blank=True, default='', max_length=200)),
                ('fuel_type', models.CharField(
                    blank=True, default='', max_length=100)),
                ('gauge', models.CharField(blank=True, default='', max_length=175)),
                ('gear_ratio', models.CharField(
                    blank=True, default='', max_length=100)),
                ('generator', models.CharField(
                    blank=True, default='', max_length=150)),
                ('heating_area', models.CharField(
                    blank=True, default='', max_length=200)),
                ('heating_surface', models.CharField(
                    blank=True, default='', max_length=200)),
                ('heating_surface_firebox', models.CharField(
                    blank=True, default='', max_length=200)),
                ('heating_surface_tubes_flues', models.CharField(
                    blank=True, default='', max_length=200)),
                ('heating_surface_tubes', models.CharField(
                    blank=True, default='', max_length=200)),
                ('heating_surface_flues', models.CharField(
                    blank=True, default='', max_length=200)),
                ('height', models.CharField(blank=True, default='', max_length=200)),
                ('height_pantograph', models.CharField(
                    blank=True, default='', max_length=100)),
                ('high_pressure_cylinder', models.CharField(
                    blank=True, default='', max_length=200)),
                ('leading_diameter', models.CharField(
                    blank=True, default='', max_length=200)),
                ('length_over_beams', models.CharField(
                    blank=True, default='', max_length=200)),
                ('length', models.CharField(blank=True, default='', max_length=200)),
                ('loco_brake', models.CharField(
                    blank=True, default='', max_length=200)),
                ('loco_weight', models.CharField(
                    blank=True, default='', max_length=250)),
                ('low_pressure_cylinder', models.CharField(
                    blank=True, default='', max_length=200)),
                ('lubricant_capacity', models.CharField(
                    blank=True, default='', max_length=100)),
                ('model', models.CharField(blank=True, default='', max_length=100)),
                ('maximum_speed', models.CharField(
                    blank=True, default='', max_length=200)),
                ('minimum_curve', models.CharField(
                    blank=True, default='', max_length=200)),
                ('mu_working', models.CharField(
                    blank=True, default='', max_length=200)),
                ('nicknames', models.CharField(
                    blank=True, default='', max_length=200)),
                ('number_in_class', models.CharField(
                    blank=True, default='', max_length=200)),
                ('number_rebuilt', models.CharField(
                    blank=True, default='', max_length=200)),
                ('numbers', models.CharField(blank=True, default='', max_length=700)),
                ('official_name', models.CharField(
                    blank=True, default='', max_length=200)),
                ('order_number', models.CharField(
                    blank=True, default='', max_length=200)),
                ('pivot_centres', models.CharField(
                    blank=True, default='', max_length=200)),
                ('power_class', models.CharField(
                    blank=True, default='', max_length=200)),
                ('power_output', models.CharField(
                    blank=True, default='', max_length=200)),
                ('power_output_one_hour', models.CharField(
                    blank=True, default='', max_length=200)),
                ('power_output_continuous', models.CharField(
                    blank=True, default='', max_length=200)),
                ('power_output_starting', models.CharField(
                    blank=True, default='', max_length=200)),
                ('power_type', models.CharField(
                    blank=True, default='', max_length=200)),
                ('prime_mover', models.CharField(
                    blank=True, default='', max_length=200)),
                ('rebuild_date', models.CharField(
                    blank=True, default='', max_length=200)),
                ('remanufacturer', models.CharField(
                    blank=True, default='', max_length=200)),
                ('retired', models.CharField(blank=True, default='', max_length=200)),
                ('rpm_range', models.CharField(
                    blank=True, default='', max_length=200)),
                ('safety_systems', models.CharField(
                    blank=True, default='', max_length=200)),
                ('serial_number', models.CharField(
                    blank=True, default='', max_length=250)),
                ('superheater_type', models.CharField(
                    blank=True, default='', max_length=200)),
                ('tender_capacity', models.CharField(
                    blank=True, default='', max_length=200)),
                ('tender_type', models.CharField(
                    blank=True, default='', max_length=200)),
                ('tender_weight', models.CharField(
                    blank=True, default='', max_length=300)),
                ('total_weight', models.CharField(
                    blank=True, default='', max_length=200)),
                ('tractive_effort', models.CharField(
                    blank=True, default='', max_length=1000)),
                ('traction_motors', models.CharField(
                    blank=True, default='', max_length=200)),
                ('trailing_diameter', models.CharField(
                    blank=True, default='', max_length=200)),
                ('train_brakes', models.CharField(
                    blank=True, default='', max_length=200)),
                ('train_heating', models.CharField(
                    blank=True, default='', max_length=200)),
                ('transmission', models.CharField(
                    blank=True, default='', max_length=200)),
                ('UIC', models.CharField(blank=True, default='', max_length=200)),
                ('valve_gear', models.CharField(
                    blank=True, default='', max_length=200)),
                ('valve_type', models.CharField(
                    blank=True, default='', max_length=200)),
                ('water_capacity', models.CharField(
                    blank=True, default='', max_length=300)),
                ('wheel_configuration_aar', models.CharField(
                    blank=True, default='', max_length=200)),
                ('wheel_configuration_commonwealth', models.CharField(
                    blank=True, default='', max_length=200)),
                ('wheelbase', models.CharField(
                    blank=True, default='', max_length=200)),
                ('wheelbase_engine', models.CharField(
                    blank=True, default='', max_length=200)),
                ('wheelbase_tender', models.CharField(
                    blank=True, default='', max_length=200)),
                ('wheel_diameter', models.CharField(
                    blank=True, default='', max_length=200)),
                ('whyte', models.CharField(blank=True, default='', max_length=200)),
                ('width', models.CharField(blank=True, default='', max_length=200)),
                ('withdrawn', models.CharField(
                    blank=True, default='', max_length=200)),
                ('post_fk', models.ForeignKey(blank=True, default=None, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, to='notes.post')),
            ],
            options={
                'verbose_name': 'Locomotive Class',
                'verbose_name_plural': 'Locomotive Classes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='WheelArrangement',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('uic_system', models.CharField(blank=True,
                 db_column='UIC_system', max_length=20, null=True)),
                ('whyte_notation', models.CharField(blank=True,
                 db_column='Whyte_notation', max_length=20, null=True)),
                ('american_name', models.CharField(blank=True,
                 db_column='American_name', max_length=75, null=True)),
                ('visual', models.CharField(blank=True,
                 db_column='Visual', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Locomotive',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(
                    blank=True, max_length=500, null=True)),
                ('number_as_built', models.CharField(
                    blank=True, max_length=20, null=True)),
                ('number_pregrouping', models.CharField(
                    blank=True, max_length=20, null=True)),
                ('number_grouping', models.CharField(
                    blank=True, max_length=20, null=True)),
                ('number_postgrouping', models.CharField(
                    blank=True, max_length=20, null=True)),
                ('brd_slug', models.CharField(blank=True, max_length=250, null=True)),
                ('brd_order_number_slug', models.CharField(
                    blank=True, max_length=250, null=True)),
                ('works_number', models.CharField(
                    blank=True, max_length=30, null=True)),
                ('brd_class_name', models.CharField(
                    blank=True, max_length=250, null=True)),
                ('brd_class_name_slug', models.CharField(
                    blank=True, max_length=250, null=True)),
                ('order_number', models.CharField(
                    blank=True, max_length=20, null=True)),
                ('order_date', models.CharField(
                    blank=True, max_length=10, null=True)),
                ('order_datetime', models.DateField(blank=True, null=True)),
                ('build_date', models.CharField(
                    blank=True, max_length=10, null=True)),
                ('build_datetime', models.DateField(blank=True, null=True)),
                ('manufacturer', models.CharField(
                    blank=True, max_length=50, null=True)),
                ('withdrawn_date', models.CharField(
                    blank=True, max_length=10, null=True)),
                ('withdrawn_datetime', models.DateField(blank=True, null=True)),
                ('scrapped_date', models.CharField(
                    blank=True, max_length=10, null=True)),
                ('scrapped_datetime', models.DateField(blank=True, null=True)),
                ('company_grouping_code', models.CharField(
                    blank=True, max_length=10, null=True)),
                ('company_pregrouping_code', models.CharField(
                    blank=True, max_length=10, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('lococlass', models.ForeignKey(blank=True, default=None, null=True,
                 on_delete=django.db.models.deletion.SET_DEFAULT, to='locos.lococlass', verbose_name='Locomotive Class')),
                ('post_fk', models.ForeignKey(blank=True, default=None, null=True,
                 on_delete=django.db.models.deletion.SET_NULL, to='notes.post')),
            ],
        ),
        migrations.CreateModel(
            name='LocoClassList',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=1000)),
                ('wikislug', models.SlugField(allow_unicode=True,
                 blank=True, default=None, max_length=250, null=True)),
                ('brdslug', models.CharField(default=None, max_length=255, null=True)),
                ('lococlass_fk', models.ForeignKey(blank=True, null=True,
                 on_delete=django.db.models.deletion.CASCADE, to='locos.lococlass')),
            ],
            options={
                'verbose_name': 'Locomotive Class Mapping',
                'verbose_name_plural': 'Locomotive Class Mappings',
            },
        ),
        migrations.AddField(
            model_name='lococlass',
            name='wheel_arrangement',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT,
                                    to='locos.wheelarrangement', verbose_name='Wheel Arrangement'),
        ),
    ]
