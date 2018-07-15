from datetime import date
from datetime import timedelta

from django.core import management
from django.core.management.base import BaseCommand

from channels.models import Channel


class Command(BaseCommand):
    help = 'Update all channels on the database.'

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=1)
        channels = Channel.objects.filter(updated__lte=yesterday).order_by("-updated")
        for channel in channels:
            management.call_command("update_channel", channel.youtube_url)
