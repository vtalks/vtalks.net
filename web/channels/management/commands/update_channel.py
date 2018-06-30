from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from channels.management import channel
from channels.models import Channel

from youtube_data_api3.channel import get_channel_code
from youtube_data_api3.channel import fetch_channel_data


class Command(BaseCommand):
    help = 'Updates a youtube Channel into the database, given its Youtube URL'

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

        # Check if the playlist is already on the database
        if not Channel.objects.filter(code=channel_code).exists():
            msg = "ERROR: Channel {:s} is not present on the database".format(channel_code)
            self.stdout.write(self.style.NOTICE(msg))

            # Call to create command instead
            management.call_command("create_channel", youtube_url_channel)

        # Get the channel from the database
        channel_obj = Channel.objects.get(code=channel_code)

        msg = "Updating channel code:{:s}".format(channel_obj.code)
        self.stdout.write(msg)

        # Fetch channel data from Youtube API
        channel_json_data = fetch_channel_data(settings.YOUTUBE_API_KEY, channel_obj.code)

        # If no data is received do nothing
        if channel_json_data is None:
            msg = "ERROR: Youtube Data API does not return anything for channel {:s}".format(channel_obj.code)
            self.stdout.write(self.style.ERROR(msg))
            exit(1)

        channel.update_channel(channel_obj, channel_json_data)

        msg = "Channel id:{:d} - title:{:s} updated successfully".format(channel_obj.id, channel_obj.title)
        self.stdout.write(self.style.SUCCESS(msg))
