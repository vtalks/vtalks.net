# Generated by Django 2.0 on 2018-01-02 14:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0019_auto_20180102_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='code',
            field=models.CharField(default=None, max_length=100, unique=True),
        ),
    ]