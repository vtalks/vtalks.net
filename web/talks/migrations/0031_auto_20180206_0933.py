# Generated by Django 2.0.1 on 2018-02-06 09:33

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('talks', '0030_talk_event_edition'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='talklike',
            unique_together={('user', 'talk')},
        ),
    ]
