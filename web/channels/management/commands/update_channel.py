from django.conf import settings
from django.core import management
from django.utils import timezone
from django.core.management.base import BaseCommand

from channels.management import channel
from channels.models import Channel

from youtube_data_api3.channel import get_channel_code
from youtube_data_api3.channel import fetch_channel_data


class Command(BaseCommand):
    help = 'Updates an existing Channel into the database, given its Youtube URL'

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
            return

        # Check if the channel is already on the database
        if not Channel.objects.filter(code=channel_code).exists():
            msg = "ERROR: Channel {:s} is not present on the database".format(channel_code)
            self.stdout.write(self.style.NOTICE(msg))

            # Call to create command instead
            management.call_command("create_channel", youtube_url_channel)
            return

        # Get the channel from the database
        channel_obj = Channel.objects.get(code=channel_code)

        delta = timezone.now() - channel_obj.updated
        if delta.total_seconds() <= settings.UPDATE_THRESHOLD:
            msg = "Channel code:{:s} have been updated in the last 24h seconds:{:f}".format(channel_obj.code, delta.total_seconds())
            self.stdout.write(msg)
            return

        msg = "Updating channel code:{:s}".format(channel_obj.code)
        self.stdout.write(msg)

        # Fetch channel data from Youtube API
        channel_json_data = fetch_channel_data(settings.YOUTUBE_API_KEY, channel_obj.code)

        # If no data is received do nothing
        if channel_json_data is None:
            msg = "ERROR: Youtube Data API does not return anything for channel {:s}".format(channel_obj.code)
            self.stdout.write(self.style.ERROR(msg))
            return

        channel.update_channel(channel_obj, channel_json_data)

        msg = "Channel id:{:d} - title:{:s} updated successfully".format(channel_obj.id, channel_obj.title)
        self.stdout.write(self.style.SUCCESS(msg))
