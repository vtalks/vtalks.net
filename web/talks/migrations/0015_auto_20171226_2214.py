# Generated by Django 2.0 on 2017-12-26 22:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0014_auto_20171226_2212'),
    ]

    operations = [
        migrations.AlterField(
            model_name='channel',
            name='slug',
            field=models.SlugField(default=None, max_length=200, unique=True),
        ),
    ]
