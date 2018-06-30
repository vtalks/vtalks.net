from django.core import management
from django.core.management.base import BaseCommand

from channels.models import Channel


class Command(BaseCommand):
    help = 'Update all channels on the database.'

    def handle(self, *args, **options):
        channels = Channel.objects.all()
        for channel in channels:
            management.call_command("update_channel", channel.youtube_url)
