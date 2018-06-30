from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from playlists.management import playlist
from playlists.models import Playlist

from youtube_data_api3.playlist import get_playlist_code
from youtube_data_api3.playlist import fetch_playlist_data


class Command(BaseCommand):
    help = 'Updates an existing Playlist into the database, given its Youtube URL'

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
        if not Playlist.objects.filter(code=playlist_code).exists():
            msg = "ERROR: Playlist {:s} is not present on the database".format(playlist_code)
            self.stdout.write(self.style.NOTICE(msg))

            # Call to create command instead
            management.call_command("create_playlist", youtube_url_playlist)
            return

        # Get the playlist from the database
        playlist_obj = Playlist.objects.get(code=playlist_code)

        msg = "Updating playlist code:{:s}".format(playlist_obj.code)
        self.stdout.write(msg)

        # Fetch playlist data from Youtube API
        playlist_json_data = fetch_playlist_data(settings.YOUTUBE_API_KEY, playlist_obj.code)

        # If no data is received do nothing
        if playlist_json_data is None:
            msg = "ERROR: Youtube Data API does not return anything for playlist {:s}".format(playlist_obj.code)
            self.stdout.write(self.style.ERROR(msg))
            return

        playlist.update_playlist(playlist_obj, playlist_json_data)

        msg = "Playlist id:{:d} - title:{:s} updated successfully".format(playlist_obj.id, playlist_obj.title)
        self.stdout.write(self.style.SUCCESS(msg))

    """
        # Fetch playlist items data from Youtube API
        youtube_playlist_items_data = fetch_playlist_items(settings.YOUTUBE_API_KEY, playlist.code)

        # If no data is received do nothing
        if youtube_playlist_items_data is None:
            print("ERROR: Youtube Data API does not return anything for playlist items {:s}".format(playlist_code))
            exit(1)

        print("{:d} videos on {:s} playlist".format(len(youtube_playlist_items_data), playlist.code))

        for video_code in youtube_playlist_items_data:
            if not Talk.objects.filter(code=video_code).exists():
                self.create_video(video_code, playlist)
            self.update_video(video_code)

    def create_update_channel(self, channel_code):
        youtube_channel_data = fetch_channel_data(settings.YOUTUBE_API_KEY, channel_code)

        published_at = youtube_channel_data["snippet"]["publishedAt"]
        datetime_published_at = datetime.strptime(published_at,"%Y-%m-%dT%H:%M:%S.000Z")
        datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)

        # Create or Update Channel
        channel, created = Channel.objects.update_or_create(
            code=youtube_channel_data["id"],
            defaults={
                'code': youtube_channel_data["id"],
                'title': youtube_channel_data["snippet"]["title"],
                'description': youtube_channel_data["snippet"]["description"],
                'created': datetime_published_at,
                'updated': timezone.now(),
            },
        )
        if created:
            print("Created channel {:s} successfully".format(channel_code))
        else:
            print("Updated channel {:s} successfully".format(channel_code))

        return channel

    def create_video(self, video_code, playlist):
        print("Creating video code:{:s}".format(video_code))

        # Fetch video data from Youtube API
        youtube_video_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        # If no data is received do nothing
        if youtube_video_data is None:
            print("ERROR: Youtube Data API does not return anything for playlist {:s}".format(video_code))
            return

        # Create or update channel
        channel_code = youtube_video_data["snippet"]["channelId"]
        channel = self.create_update_channel(channel_code)

        published_at = youtube_video_data["snippet"]["publishedAt"]
        datetime_published_at = datetime.strptime(published_at,"%Y-%m-%dT%H:%M:%S.000Z")
        datetime_published_at = datetime_published_at.replace(tzinfo=timezone.utc)

        # Create playlist
        talk = Talk.objects.create(
            code=youtube_video_data["id"],
            title=youtube_video_data["snippet"]["title"],
            description=youtube_video_data["snippet"]["description"],
            channel=channel,
            playlist=playlist,
            created=datetime_published_at,
            updated=timezone.now(),
        )

        print("Talk created successfully")

    def update_video(self, video_code):
        # Get talk from the database
        talk = None
        try:
            talk = Talk.objects.get(code=video_code)
        except Talk.DoesNotExist:
            print("ERROR: Video does not exist on the database")
            return

        print("Updating video id:{:d} - code:{:s} - youtube_url:{:s}".format(
            talk.id,
            talk.code,
            talk.youtube_url)
        )

        # Fetch video data from Youtube API
        youtube_video_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        # if no data is received we un-publish the video
        if youtube_video_data is None:
            print("Un-publish video because youtube API does not return data")
            talk.published = False
            talk.save()
            return

        # if uploadStatus on youtube is failed we un-publish the video
        if "status" in youtube_video_data:
            status = youtube_video_data['status']
            if "uploadStatus" in status:
                if status['uploadStatus'] == "failed":
                    print("Un-publish video because youtube statusUpload is failed")
                    talk.published = False
                    talk.save()
                    return

        talk.update_video_model(youtube_video_data)

        talk.update_video_tags(youtube_video_data)

        talk.update_video_statistics(youtube_video_data)

        talk.recalculate_video_sortrank()

        talk.save()

        print("Video updated successfully")
    """