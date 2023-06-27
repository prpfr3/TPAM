# Generated by Django 3.2.1 on 2023-06-20 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0006_auto_20230617_0839'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='person',
            name='role',
        ),
        migrations.CreateModel(
            name='PersonRole',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_from', models.CharField(blank=True, default='', max_length=10)),
                ('date_to', models.CharField(blank=True, default='', max_length=10)),
                ('person', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.person')),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='people.role')),
            ],
            options={
                'verbose_name': 'Person Role',
                'verbose_name_plural': 'People Role',
            },
        ),
        migrations.AddField(
            model_name='person',
            name='roles',
            field=models.ManyToManyField(blank=True, through='people.PersonRole', to='people.Role'),
        ),
    ]
