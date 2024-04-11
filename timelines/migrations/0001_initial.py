# Generated by Django 3.2.1 on 2024-02-06 11:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TimelineSlide',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('media_caption', models.CharField(blank=True, default='', max_length=100)),
                ('media_credit', models.CharField(blank=True, default='', max_length=200)),
                ('media_url', models.URLField(blank=True, default='', max_length=400)),
                ('text_headline', models.CharField(blank=True, max_length=200, null=True)),
                ('text_text', models.TextField(blank=True, null=True)),
                ('wikipedia_name', models.CharField(blank=True, default='', max_length=1000)),
                ('start_date', models.CharField(blank=True, default='', max_length=10)),
                ('end_date', models.CharField(blank=True, default='', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='TimelineSlideHeader',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(blank=True, default=None, help_text='Enter a slug only if you wish to override that which will be autogenerated from the text headline.', max_length=255, null=True, unique=True)),
                ('media_caption', models.CharField(blank=True, default='', max_length=100)),
                ('media_credit', models.CharField(blank=True, default='', max_length=200)),
                ('media_url', models.URLField(blank=True, default='', max_length=300)),
                ('text_headline', models.CharField(blank=True, max_length=200, null=True)),
                ('text_text', models.TextField(blank=True, null=True)),
                ('type', models.CharField(default='overview', max_length=20)),
                ('wikipedia_name', models.CharField(blank=True, default='', max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='TimelineSlidepack',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slide_order', models.SmallIntegerField()),
                ('slide_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timelines.timelineslide')),
                ('slideheader_fk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='timelines.timelineslideheader')),
            ],
        ),
        migrations.AddField(
            model_name='timelineslide',
            name='slideheader',
            field=models.ManyToManyField(related_name='slidepack_slide', through='timelines.TimelineSlidepack', to='timelines.TimelineSlideHeader'),
        ),
    ]