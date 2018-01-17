# Generated by Django 2.0.1 on 2018-01-16 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_profile', '0008_auto_20171218_1815'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='userprofile',
            options={'get_latest_by': ['-user__created'], 'ordering': ['-user__created'], 'verbose_name': 'Profile', 'verbose_name_plural': 'Profiles'},
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='twitter_id',
            field=models.CharField(blank=True, max_length=100, verbose_name='Twitter ID'),
        ),
    ]