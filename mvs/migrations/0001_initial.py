# Generated by Django 3.2.1 on 2023-03-23 11:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Fav',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'Military Vehicle Favourite',
                'verbose_name_plural': 'Military Vehicle Favourites',
            },
        ),
        migrations.CreateModel(
            name='HeritageSite',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(default=None, max_length=100)),
                ('wikislug', models.SlugField(allow_unicode=True,
                 blank=True, default=None, max_length=250, null=True)),
                ('url', models.URLField(default=None, null=True)),
                ('notes', models.TextField(default=None, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='MilitaryVehicleClass',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('mvclass', models.CharField(blank=True,
                 default=None, max_length=100, null=True)),
                ('wikislug', models.SlugField(allow_unicode=True,
                 blank=True, default=None, max_length=250, null=True)),
                ('description', models.CharField(blank=True,
                 default=None, max_length=500, null=True)),
                ('notes', models.TextField(blank=True, default=None, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('favorites', models.ManyToManyField(
                    related_name='favorite_things', through='mvs.Fav', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Military Vehicle Class',
                'verbose_name_plural': 'Military Vehicle Classes',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Visit',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('notes', models.TextField(default=None)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT,
                 to='mvs.heritagesite', verbose_name='Location')),
            ],
        ),
        migrations.CreateModel(
            name='MVImage',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('image_name', models.CharField(default=None, max_length=100)),
                ('image', models.ImageField(upload_to='images/')),
                ('notes', models.TextField(blank=True, default=None, null=True)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
                ('location', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT,
                 to='mvs.heritagesite', verbose_name='Location')),
                ('mvclass', models.ForeignKey(default=1, on_delete=django.db.models.deletion.SET_DEFAULT,
                 to='mvs.militaryvehicleclass', verbose_name='Military Vehicle Class')),
                ('visit', models.ForeignKey(
                    default=1, on_delete=django.db.models.deletion.SET_DEFAULT, to='mvs.visit', verbose_name='Visit')),
            ],
            options={
                'verbose_name': 'Military Vehicle Image',
                'verbose_name_plural': 'Military Vehicle Images',
            },
        ),
        migrations.CreateModel(
            name='MVBMImage',
            fields=[
                ('id', models.AutoField(auto_created=True,
                 primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('url', models.URLField()),
                ('image', models.ImageField(upload_to='images/%Y/%m/%d/')),
                ('description', models.TextField(blank=True)),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                 related_name='mvimages_created', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True,
                 related_name='mvimages_liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Military Vehicle Bookmarked Image',
                'verbose_name_plural': 'Military Vehicle Bookmarked Images',
            },
        ),
        migrations.AddField(
            model_name='fav',
            name='thing',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to='mvs.militaryvehicleclass'),
        ),
        migrations.AddField(
            model_name='fav',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE,
                                    related_name='favs_users', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='fav',
            unique_together={('thing', 'user')},
        ),
    ]
