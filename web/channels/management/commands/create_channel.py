from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from channels.management import channel
from channels.models import Channel

from youtube_data_api3.channel import get_channel_code
from youtube_data_api3.channel import fetch_channel_data


class Command(BaseCommand):
    help = 'Create a youtube Channel into the database, given its Youtube URL'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url_channel', type=str)

    def handle(self, *args, **options):
        youtube_url_channel = options['youtube_url_channel']

        # Get code from youtube url
        channel_code = ""
        try:
            channel_code = get_channel_code(youtube_url_channel)
        except Exception:
            msg = "ERROR: Invalid URL channel {:s}".format(youtube_url_channel)
            self.stdout.write(self.style.ERROR(msg))
            exit(1)

        if Channel.objects.filter(code=channel_code).exists():
            msg = "ERROR: Channel {:s} is already present on the database".format(channel_code)
            self.stdout.write(self.style.NOTICE(msg))

            # Call to update command instead
            management.call_command("update_channel", youtube_url_channel)
            exit(0)

        msg = "Creating channel code:{:s}".format(channel_code)
        self.stdout.write(msg)

        # Fetch channel data from Youtube API
        channel_json_data = fetch_channel_data(settings.YOUTUBE_API_KEY, channel_code)

        # If no data is received do nothing
        if channel_json_data is None:
            msg = "ERROR: Youtube Data API does not return anything for channel {:s}".format(channel_code)
            self.stdout.write(self.style.ERROR(msg))
            exit(1)

        channel_obj = channel.create_channel(channel_json_data)

        msg = "Created channel id:{:d} - title:{:s} successfully".format(channel_obj.id, channel_obj.title)
        self.stdout.write(self.style.SUCCESS(msg))
