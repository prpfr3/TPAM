# Generated by Django 3.2.1 on 2022-01-11 10:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locos', '0019_auto_20220111_0719'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassDesigner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('builder_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locos.builder')),
                ('company_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locos.company')),
                ('lococlass_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='locos.lococlass')),
                ('person_fk', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='locos.person')),
            ],
        ),
    ]