from django.conf import settings
from django.core.management.base import BaseCommand

from channels.models import Channel

from youtube_data_api3.channel import get_channel_code
from youtube_data_api3.channel import fetch_channel_data


class Command(BaseCommand):
    help = 'Create a youtube Channel into the database, given its Youtube URL'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url_channel', type=str)

    def handle(self, *args, **options):
        youtube_url_channel = options['youtube_url_channel']
        pass