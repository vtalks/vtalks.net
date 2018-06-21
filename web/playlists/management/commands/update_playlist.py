from django.conf import settings
from django.core.management.base import BaseCommand

from playlists.models import Playlist
from youtube_data_api3.playlist import get_playlist_code
from youtube_data_api3.playlist import fetch_playlist_data


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
        playlist = None
        try:
            playlist = Playlist.objects.get(code=playlist_code)
        except Playlist.DoesNotExist:
            print("ERROR: Playlist {:s} is not present on the database".format(playlist_code))
            exit(1)

        print("Updating playlist id:{:d} - code:{:s} - youtube_url:{:s}".format(
            playlist.id,
            playlist_code,
            youtube_url_playlist)
        )

        # Fetch playlist data from Youtube API
        youtube_playlist_data = fetch_playlist_data(settings.YOUTUBE_API_KEY, playlist_code)

        # If no data is received do nothing
        if youtube_playlist_data is None:
            print("ERROR: Youtube Data API does not return anything for playlist {:s}".format(playlist_code))
            exit(1)

        playlist.update_playlist_model(youtube_playlist_data)

        playlist.save()

        print("Playlist updated successfully")

        """
        # Add playlist
        playlist_data = fetch_playlist_data(settings.YOUTUBE_API_KEY, playlist_code)
        playlist_obj = None
        if playlist_data:
            playlist_obj, created = Playlist.objects.update_or_create(
                code=playlist_data["id"],
                defaults={
                    'code': playlist_data["id"],
                    'title': playlist_data["snippet"]["title"],
                    'description': playlist_data["snippet"]["description"],
                    'created': playlist_data["snippet"]["publishedAt"],
                    'updated': timezone.now(),
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Added playlist "%s"' % playlist_obj.title))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Updated playlist "%s"' % playlist_obj.title))

        playlist_videos = fetch_playlist_items(settings.YOUTUBE_API_KEY, playlist_code)
        for video_code in playlist_videos:
            talk_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

            # Check if there is data (private videos do not returns anything)
            if talk_data:
                channel_code = talk_data["snippet"]["channelId"]
                channel_data = fetch_channel_data(settings.YOUTUBE_API_KEY, channel_code)

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
                if created:
                    self.stdout.write('\t\tAdded talk "%s"' % talk_obj.title)
                else:
                    self.stdout.write('\t\tUpdated talk "%s"' % talk_obj.title)

                # Add tags from cli arguments and talk_data
                video_tags = []
                if "tags" in talk_data["snippet"]:
                    video_tags += talk_data["snippet"]["tags"]
                for tag in video_tags:
                    talk_obj.tags.add(tag)
                    self.stdout.write('\t\t\tTagged as "%s"' % tag)

                hours = 0
                minutes = 0
                seconds = 0
                duration = talk_data["contentDetails"]["duration"]
                try:
                    hours = re.compile('(\d+)H').search(duration).group(1)
                except AttributeError:
                    hours = 0
                try:
                    minutes = re.compile('(\d+)M').search(duration).group(1)
                except AttributeError:
                    minutes = 0
                try:
                    seconds = re.compile('(\d+)S').search(duration).group(1)
                except AttributeError:
                    seconds = 0

                d = timedelta(hours=int(hours), minutes=int(minutes),
                              seconds=int(seconds))
                talk_obj.duration = d

                talk_obj.save()
        """
