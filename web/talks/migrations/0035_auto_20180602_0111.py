# Generated by Django 2.0.6 on 2018-06-02 01:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0034_auto_20180223_0911'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
