# Generated by Django 3.2.1 on 2021-06-24 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('maps', '0011_rename_author_post_owner'),
    ]

    operations = [
        migrations.CreateModel(
            name='Depots',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('depot', models.CharField(blank=True, max_length=500, null=True)),
                ('codes', models.CharField(blank=True, max_length=100, null=True)),
                ('code_dates', models.CharField(blank=True, max_length=100, null=True)),
                ('date_opened', models.CharField(blank=True, max_length=20, null=True)),
                ('date_closed_to_steam', models.CharField(blank=True, max_length=20, null=True)),
                ('date_closed', models.CharField(blank=True, max_length=20, null=True)),
                ('pre_grouping_company', models.CharField(blank=True, max_length=20, null=True)),
                ('grouping_company', models.CharField(blank=True, max_length=20, null=True)),
                ('br_region', models.CharField(blank=True, db_column='BR_region', max_length=20, null=True)),
                ('map', models.CharField(blank=True, max_length=200, null=True)),
                ('web', models.CharField(blank=True, max_length=200, null=True)),
                ('comments', models.TextField()),
                ('image', models.ImageField(default=None, upload_to='images/')),
            ],
            options={
                'verbose_name_plural': 'Depots',
            },
        ),
        migrations.CreateModel(
            name='Engineer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('eng_name', models.CharField(default=None, max_length=100)),
                ('wikislug', models.SlugField(default=None)),
                ('url', models.URLField(default=None)),
                ('notes', models.TextField(default=None)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='HeritageLocoSeen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loco_status', models.IntegerField(choices=[(1, 'In Steam'), (2, 'Out of Service')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='HeritageSite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default=None, max_length=100)),
                ('wikislug', models.SlugField(default=None, max_length=255, null=True)),
                ('url', models.URLField(default=None, null=True)),
                ('notes', models.TextField(default=None, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(default=None, max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('notes', models.TextField(default=None)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='maps.heritagesite', verbose_name='Location')),
            ],
        ),
        migrations.CreateModel(
            name='LocoClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grouping_company', models.CharField(blank=True, default='', max_length=10)),
                ('pre_grouping_company', models.CharField(blank=True, default='', max_length=20)),
                ('designer', models.CharField(blank=True, default='', max_length=100)),
                ('designer_slug', models.SlugField(max_length=255, null=True)),
                ('grouping_class', models.CharField(blank=True, default='', max_length=100)),
                ('grouping_class_slug', models.SlugField(default=None, max_length=255, null=True)),
                ('pre_grouping_class', models.CharField(blank=True, default='', max_length=100)),
                ('br_power_class', models.CharField(blank=True, default='', max_length=5)),
                ('wheel_body_type', models.CharField(blank=True, default='', max_length=100)),
                ('year_built', models.CharField(blank=True, default='', max_length=100)),
                ('number_range', models.CharField(blank=True, default='', max_length=100)),
                ('number_range_slug', models.SlugField(default=None, max_length=255, null=True)),
                ('year_first_built', models.CharField(blank=True, default='', max_length=100)),
                ('year_last_built', models.CharField(blank=True, default='', max_length=100)),
                ('number_built', models.CharField(blank=True, default='', max_length=100)),
                ('img_slug', models.SlugField(default=None, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Locomotive Classes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Manufacturers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('manufacturer_code', models.CharField(blank=True, max_length=3, null=True)),
                ('manufacturer_name', models.CharField(blank=True, max_length=50, null=True)),
                ('location', models.CharField(blank=True, max_length=200, null=True)),
                ('date_opened', models.CharField(blank=True, max_length=10, null=True)),
                ('date_closed', models.CharField(blank=True, max_length=10, null=True)),
                ('type', models.CharField(blank=True, max_length=77, null=True)),
                ('steam', models.CharField(blank=True, max_length=10, null=True)),
                ('diesel', models.CharField(blank=True, max_length=10, null=True)),
                ('electric', models.CharField(blank=True, max_length=10, null=True)),
                ('map', models.CharField(blank=True, max_length=200, null=True)),
                ('web', models.CharField(blank=True, max_length=200, null=True)),
            ],
            options={
                'verbose_name_plural': 'Manufacturers',
            },
        ),
        migrations.CreateModel(
            name='ModernClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('class_type', models.CharField(blank=True, default='', max_length=1)),
                ('modern_class', models.CharField(blank=True, default='', max_length=100)),
                ('modern_class_slug', models.SlugField(default=None, max_length=255, null=True)),
                ('aka_class', models.CharField(blank=True, default='', max_length=100)),
                ('aka_class_slug', models.SlugField(default=None, max_length=255, null=True)),
                ('year_introduced', models.CharField(blank=True, default='', max_length=100)),
                ('manufacturer', models.CharField(blank=True, default='', max_length=100)),
                ('power_unit', models.CharField(blank=True, default='', max_length=100)),
                ('horse_power', models.CharField(blank=True, default='', max_length=100)),
                ('current', models.CharField(blank=True, default='', max_length=100)),
                ('wheel_id', models.CharField(blank=True, default='', max_length=100)),
                ('wheel_id_slug', models.SlugField(default=None, max_length=255, null=True)),
                ('transmission', models.CharField(blank=True, default='', max_length=50)),
                ('number_range', models.CharField(blank=True, default='', max_length=255)),
                ('number_range_slug', models.SlugField(default=None, max_length=255, null=True)),
                ('number_built', models.CharField(blank=True, default='', max_length=100)),
                ('multiple', models.CharField(blank=True, default='', max_length=100)),
                ('img_slug', models.SlugField(default=None, max_length=255, null=True)),
            ],
            options={
                'verbose_name_plural': 'Post Steam Locomotive Classes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='WheelArrangement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uic_system', models.CharField(blank=True, db_column='UIC_system', max_length=20, null=True)),
                ('whyte_notation', models.CharField(blank=True, db_column='Whyte_notation', max_length=20, null=True)),
                ('american_name', models.CharField(blank=True, db_column='American_name', max_length=75, null=True)),
                ('visual', models.CharField(blank=True, db_column='Visual', max_length=20, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('notes', models.TextField(default=None)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='locos.heritagesite', verbose_name='Location')),
            ],
        ),
        migrations.CreateModel(
            name='Locomotive',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('build_date', models.CharField(blank=True, max_length=10, null=True)),
                ('pre_grouping_class', models.CharField(blank=True, max_length=10, null=True)),
                ('number', models.CharField(blank=True, max_length=20, null=True)),
                ('wheel_arrangement', models.CharField(blank=True, max_length=10, null=True)),
                ('designer', models.CharField(blank=True, max_length=30, null=True)),
                ('manufacturer', models.CharField(blank=True, max_length=50, null=True)),
                ('order_number', models.CharField(blank=True, max_length=30, null=True)),
                ('works_number', models.CharField(blank=True, max_length=30, null=True)),
                ('withdrawn', models.CharField(blank=True, max_length=15, null=True)),
                ('images', models.ManyToManyField(through='locos.HeritageLocoSeen', to='locos.Image')),
                ('modern_class', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='locos.modernclass', verbose_name='Modern Class')),
                ('steam_class', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='locos.lococlass', verbose_name='Steam Class')),
            ],
        ),
        migrations.AddField(
            model_name='lococlass',
            name='wheel_arrangement',
            field=models.ForeignKey(blank=None, default=None, null=True, on_delete=django.db.models.deletion.SET_DEFAULT, to='locos.wheelarrangement', verbose_name='Wheel Arrangement'),
        ),
        migrations.AddField(
            model_name='image',
            name='loco_class',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='locos.lococlass', verbose_name='Locomotive Class'),
        ),
        migrations.AddField(
            model_name='image',
            name='locos',
            field=models.ManyToManyField(through='locos.HeritageLocoSeen', to='locos.Locomotive'),
        ),
        migrations.AddField(
            model_name='image',
            name='visit',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='maps.visit', verbose_name='Visit'),
        ),
        migrations.AddField(
            model_name='heritagelocoseen',
            name='image',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locos.image'),
        ),
        migrations.AddField(
            model_name='heritagelocoseen',
            name='loco',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locos.locomotive'),
        ),
    ]
