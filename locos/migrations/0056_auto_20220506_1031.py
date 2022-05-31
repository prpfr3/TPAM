# Generated by Django 3.2.1 on 2022-05-06 09:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0055_auto_20220505_1027'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lococlass',
            old_name='grouping_class',
            new_name='wikipedia_name',
        ),
        migrations.RenameField(
            model_name='lococlass',
            old_name='grouping_class_slug',
            new_name='wikipedia_slug',
        ),
        migrations.RenameField(
            model_name='locomotive',
            old_name='pre_grouping_class',
            new_name='wikipedia_name',
        ),
        migrations.RemoveField(
            model_name='depots',
            name='grouping_company',
        ),
        migrations.RemoveField(
            model_name='depots',
            name='pre_grouping_company',
        ),
        migrations.RemoveField(
            model_name='lococlass',
            name='grouping_company',
        ),
        migrations.RemoveField(
            model_name='lococlass',
            name='pre_grouping_class',
        ),
        migrations.RemoveField(
            model_name='lococlass',
            name='pre_grouping_company',
        ),
        migrations.CreateModel(
            name='LocoClassList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=500)),
                ('wikislug', models.SlugField(default=None, max_length=255, null=True)),
                ('lococlass_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locos.lococlass')),
            ],
        ),
    ]
