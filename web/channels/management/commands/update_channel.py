from django.conf import settings
from django.core.management.base import BaseCommand

from channels.models import Channel

from youtube_data_api3.channel import get_channel_code
from youtube_data_api3.channel import fetch_channel_data


class Command(BaseCommand):
    help = 'Update a youtube Channel to the database.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url_channel', type=str)

    def handle(self, *args, **options):
        youtube_url_channel = options['youtube_url_channel']

        # Get code from youtube url
        channel_code = ""
        try:
            channel_code = get_channel_code(youtube_url_channel)
        except Exception:
            print(
                "ERROR: Invalid URL channel {:s}".format(youtube_url_channel))
            exit(1)

        # Check if the playlist is already on the database
        channel = None
        try:
            channel = Channel.objects.get(code=channel_code)
        except Channel.DoesNotExist:
            print(
                "ERROR: Channel {:s} is not present on the database".format(
                    channel_code))
            exit(1)

        print("Updating channel id:{:d} - code:{:s} - youtube_url:{:s}".format(
            channel.id,
            channel_code,
            youtube_url_channel)
        )

        # Fetch channel data from Youtube API
        youtube_channel_data = fetch_channel_data(settings.YOUTUBE_API_KEY, channel_code)

        # If no data is received do nothing
        if youtube_channel_data is None:
            print("ERROR: Youtube Data API does not return anything for channel {:s}".format(channel_code))
            exit(1)

        channel.update_playlist_model(youtube_channel_data)

        channel.save()

        print("Channel updated successfully")