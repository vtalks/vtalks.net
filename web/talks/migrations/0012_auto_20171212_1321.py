# Generated by Django 2.0 on 2017-12-12 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talks', '0011_auto_20171212_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='talk',
            name='tags',
            field=models.CharField(blank=True, default='', max_length=500, null=True),
        ),
    ]
