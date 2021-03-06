# Generated by Django 2.0.1 on 2018-01-30 19:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_auto_20180130_1901'),
        ('talks', '0029_talkdislike'),
    ]

    operations = [
        migrations.AddField(
            model_name='talk',
            name='event_edition',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='events.Edition'),
        ),
    ]
