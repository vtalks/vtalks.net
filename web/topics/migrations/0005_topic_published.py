# Generated by Django 2.0.7 on 2018-07-02 20:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0004_remove_topic_elastic_search_query_dsl'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='published',
            field=models.BooleanField(default=True, verbose_name='is published'),
        ),
    ]
