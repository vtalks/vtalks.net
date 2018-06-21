from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone

from talks.models import Talk
from playlists.models import Playlist
from youtube_data_api3.playlist import get_playlist_code
from youtube_data_api3.playlist import fetch_playlist_data
from youtube_data_api3.playlist import fetch_playlist_items
from youtube_data_api3.video import fetch_video_data


class Command(BaseCommand):
    help = 'Adds all videos from a youtube playlist to the database.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url_playlist', type=str)

    def handle(self, *args, **options):
        youtube_url_playlist = options['youtube_url_playlist']

        # Get code from youtube url
        playlist_code = ""
        try:
            playlist_code = get_playlist_code(youtube_url_playlist)
        except Exception:
            print("ERROR: Invalid URL playlist {:s}".format(youtube_url_playlist))
            exit(1)

        # Check if the playlist is already on the database
        if Playlist.objects.filter(code=playlist_code).exists():
            print("ERROR: Playlist {:s} is already on the database".format(playlist_code))
            exit(1)

        print("Creating playlist code:{:s} - youtube_url:{:s}".format(
            playlist_code,
            youtube_url_playlist)
        )

        # Fetch playlist data from Youtube API
        youtube_playlist_data = fetch_playlist_data(settings.YOUTUBE_API_KEY, playlist_code)

        # If no data is received do nothing
        if youtube_playlist_data is None:
            print("ERROR: Youtube Data API does not return anything for playlist {:s}".format(playlist_code))
            exit(1)

        # Create playlist
        playlist = Playlist.objects.create(
            code=youtube_playlist_data["id"],
            title=youtube_playlist_data["snippet"]["title"],
            description=youtube_playlist_data["snippet"]["description"],
            created=youtube_playlist_data["snippet"]["publishedAt"],
            updated=timezone.now(),
        )

        print("Playlist created successfully")

        # Fetch playlist items data from Youtube API
        youtube_playlist_items_data = fetch_playlist_items(settings.YOUTUBE_API_KEY, playlist.code)

        # If no data is received do nothing
        if youtube_playlist_items_data is None:
            print("ERROR: Youtube Data API does not return anything for playlist items {:s}".format(playlist_code))
            exit(1)

        print("{:d} videos on {:s} playlist".format(len(youtube_playlist_items_data), playlist.code))

        for video_code in youtube_playlist_items_data:
            self.update_video(video_code)

        """
        for video_code in playlist_videos:
                # Add Channel
                channel_obj, created = Channel.objects.update_or_create(
                    code=channel_data["id"],
                    defaults={
                        'code': channel_data["id"],
                        'title': channel_data["snippet"]["title"],
                        'description': channel_data["snippet"]["description"],
                        'created': channel_data["snippet"]["publishedAt"],
                        'updated': timezone.now(),
                    },
                )
                if created:
                    self.stdout.write('\tAdded channel "%s"' % channel_obj.title)
                else:
                    self.stdout.write('\tUpdated channel "%s"' % channel_obj.title)

                # Add Video
                if "tags" not in talk_data["snippet"]:
                    talk_data["snippet"]["tags"] = []
                if "viewCount" not in talk_data["statistics"]:
                    talk_data["statistics"]["viewCount"] = 0
                if "likeCount" not in talk_data["statistics"]:
                    talk_data["statistics"]["likeCount"] = 0
                if "dislikeCount" not in talk_data["statistics"]:
                    talk_data["statistics"]["dislikeCount"] = 0
                if "favoriteCount" not in talk_data["statistics"]:
                    talk_data["statistics"]["favoriteCount"] = 0

                talk_obj, created = Talk.objects.update_or_create(
                    code=talk_data["id"],
                    defaults={
                        'code': talk_data["id"],
                        'title': talk_data["snippet"]["title"],
                        'description': talk_data["snippet"]["description"],
                        'channel': channel_obj,
                        'playlist': playlist_obj,
                        'youtube_view_count': talk_data["statistics"]["viewCount"],
                        'youtube_like_count': talk_data["statistics"]["likeCount"],
                        'youtube_dislike_count': talk_data["statistics"]["dislikeCount"],
                        'youtube_favorite_count': talk_data["statistics"]["favoriteCount"],
                        'created': datetime.strptime(talk_data["snippet"]["publishedAt"], "%Y-%m-%dT%H:%M:%S.000Z").replace(tzinfo=timezone.utc),
                        'updated': timezone.now(),
                    },
                )
        """

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