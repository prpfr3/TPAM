# Generated by Django 3.2.1 on 2023-01-24 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('locations', '0017_auto_20230124_1104'),
        ('maps', '0012_alter_post_body'),
        ('locos', '0016_reference_location_fk'),
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
        migrations.AddField(
            model_name='reference',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
        migrations.AddField(
            model_name='reference',
            name='location_description',
            field=models.CharField(blank='True', default=None, max_length=100, null='True'),
            preserve_default='True',
        ),
        migrations.AddField(
            model_name='reference',
            name='type',
            field=models.IntegerField(choices=[(1, 'Book'), (2, 'Website'), (3, 'Magazine'), (4, 'Video'), (5, 'MySighting'), (6, 'MyPhoto')], default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='reference',
            name='visit',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='maps.visit', verbose_name='Visit'),
        ),
    ]
