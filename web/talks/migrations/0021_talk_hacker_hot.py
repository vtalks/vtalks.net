# Generated by Django 2.0 on 2018-01-02 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0020_auto_20180102_1451'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='hacker_hot',
            field=models.FloatField(default=0, verbose_name='hackernews hot rank'),
        ),
    ]