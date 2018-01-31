# Generated by Django 2.0.1 on 2018-01-30 14:43

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Edition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default=None, max_length=200)),
                ('slug', models.SlugField(default=None, max_length=200, unique=True)),
                ('description', models.TextField(blank=True)),
                ('url', models.URLField(blank=True)),
                ('created', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date created')),
                ('updated', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date updated')),
            ],
            options={
                'verbose_name': 'Edition',
                'verbose_name_plural': 'Editions',
                'ordering': ['-created'],
                'get_latest_by': ['-created'],
            },
        ),
        migrations.AlterModelOptions(
            name='event',
            options={'get_latest_by': ['-created'], 'ordering': ['-created'], 'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AddField(
            model_name='edition',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='events.Event'),
        ),
    ]
