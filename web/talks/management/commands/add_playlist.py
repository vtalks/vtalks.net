from urllib.parse import urlsplit
from urllib.parse import parse_qs

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from ...models import Channel
from ...models import Talk
from ...models import fetch_channel_data
from ...models import fetch_playlist_items
from ...models import fetch_video_data

"""
TODO:

#### Open questions

* Support pagination when getting videos from a playlist
"""


def get_playlist_code(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    if "list" not in params:
        raise CommandError('Invalid url "%s"' % url)
    playlist_code = params["list"][0]
    return playlist_code


class Command(BaseCommand):
    help = 'Adds all videos from a playlist to the system.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str)
        parser.add_argument('--tags', type=str, nargs='*', help='tags to assign to videos')

    def handle(self, *args, **options):
        playlist_code = get_playlist_code(options['youtube_url'])
        playlist_videos = fetch_playlist_items(settings.YOUTUBE_API_KEY, playlist_code)
        for video_code in playlist_videos:
            talk_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

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
                self.stdout.write(
                    self.style.SUCCESS(
                        'Added channel "%s"' % channel_obj.title))
            else:
                self.stdout.write(
                    self.style.SUCCESS(
                        'Updated channel "%s"' % channel_obj.title))

            # Add Video
            if "tags" not in talk_data["snippet"]:
                talk_data["snippet"]["tags"] = []
            if "likeCount" not in talk_data["statistics"]:
                talk_data["statistics"]["likeCount"] = 0
            if "dislikeCount" not in talk_data["statistics"]:
                talk_data["statistics"]["dislikeCount"] = 0
            talk_obj, created = Talk.objects.update_or_create(
                code=talk_data["id"],
                defaults={
                    'code': talk_data["id"],
                    'title': talk_data["snippet"]["title"],
                    'description': talk_data["snippet"]["description"],
                    'channel': channel_obj,
                    'view_count': talk_data["statistics"]["viewCount"],
                    'like_count': talk_data["statistics"]["likeCount"],
                    'dislike_count': talk_data["statistics"]["dislikeCount"],
                    'created': talk_data["snippet"]["publishedAt"],
                    'updated': timezone.now(),
                },
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS('Added talk "%s"' % talk_obj.title))
            else:
                self.stdout.write(
                    self.style.SUCCESS('Updated talk "%s"' % talk_obj.title))

            # Add tags from cli arguments and talk_data
            video_tags = options['tags']
            # TODO:
            # - Add tags from youtube
            # if "tags" in talk_data["snippet"]:
            #    video_tags += talk_data["snippet"]["tags"]
            for tag in video_tags:
                talk_obj.tags.add(tag)
                self.stdout.write(self.style.SUCCESS('Tagged as "%s"' % tag))
            talk_obj.save()
