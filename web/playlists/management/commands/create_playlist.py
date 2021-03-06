from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from playlists.management import playlist
from playlists.models import Playlist
from talks.models import Talk

from youtube_data_api3.video import get_video_youtube_url
from youtube_data_api3.playlist import get_playlist_code
from youtube_data_api3.playlist import fetch_playlist_data
from youtube_data_api3.playlist import fetch_playlist_items


class Command(BaseCommand):
    help = 'Create Playlist into the database, given its Youtube URL'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url_playlist', type=str)

    def handle(self, *args, **options):
        youtube_url_playlist = options['youtube_url_playlist']

        # Get code from youtube url
        playlist_code = ""
        try:
            playlist_code = get_playlist_code(youtube_url_playlist)
        except Exception:
            msg = "ERROR: Invalid URL playlist {:s}".format(youtube_url_playlist)
            self.stdout.write(self.style.ERROR(msg))
            return

        # Check if the playlist is already on the database
        if Playlist.objects.filter(code=playlist_code).exists():
            msg = "ERROR: Playlist {:s} is already present on the database".format(playlist_code)
            self.stdout.write(self.style.NOTICE(msg))

            # Call to update command instead
            management.call_command("update_playlist", youtube_url_playlist)
            return

        msg = "Creating playlist code:{:s}".format(playlist_code)
        self.stdout.write(msg)

        # Fetch channel data from Youtube API
        playlist_json_data = fetch_playlist_data(settings.YOUTUBE_API_KEY, playlist_code)

        # If no data is received do nothing
        if playlist_json_data is None:
            msg = "ERROR: Youtube Data API does not return anything for playlist {:s}".format(playlist_code)
            self.stdout.write(self.style.ERROR(msg))
            return

        playlist_obj = playlist.create_playlist(playlist_json_data)

        msg = "Playlist id:{:d} - title:{:s} created successfully".format(playlist_obj.id, playlist_obj.title)
        self.stdout.write(self.style.SUCCESS(msg))

        # Fetch playlist items data from Youtube API
        youtube_playlist_items_data = fetch_playlist_items(settings.YOUTUBE_API_KEY, playlist_obj.code)

        # If no data is received do nothing
        if youtube_playlist_items_data is None:
            msg = "ERROR: Youtube Data API does not return anything for playlist items {:s}".format(playlist_obj.code)
            self.stdout.write(self.style.ERROR(msg))
            return

        print("{:d} talks on playlist {:s}".format(len(youtube_playlist_items_data), playlist_obj.code))

        for video_code in youtube_playlist_items_data:
            youtube_video_url = get_video_youtube_url(video_code)
            if not Talk.objects.filter(code=video_code).exists():
                management.call_command("create_talk", youtube_video_url, "--playlist={:s}".format(playlist_obj.code))
            else:
                management.call_command("update_talk", youtube_video_url, "--playlist={:s}".format(playlist_obj.code))
