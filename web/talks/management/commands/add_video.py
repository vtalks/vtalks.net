from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand

from ...models import Channel
from ...models import Talk
from ...models import fetch_channel_data
from ...models import get_video_code
from ...models import fetch_video_data

"""
TODO:

#### Open questions

* Fetch video duration from contentDetails
* Support video favoriteCount
* Support channel custom URLS
* Support channel statistics (viewCount, subscriberCount)

## Additional information

https://developers.google.com/youtube/v3/docs/channels/list
"""


class Command(BaseCommand):
    help = 'Adds a video to the system.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str)

    def handle(self, *args, **options):
        video_code = get_video_code(options['youtube_url'])
        talk_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        self.stdout.write(self.style.SUCCESS('Adding talk "%s"' % talk_data["id"]))

        channel_code = talk_data["snippet"]["channelId"]
        channel_data = fetch_channel_data(settings.YOUTUBE_API_KEY, channel_code)

        self.stdout.write(self.style.SUCCESS('Adding channel "%s"' % channel_data["id"]))

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
                self.style.SUCCESS('Added channel "%s"' % channel_obj.title))
        else:
            self.stdout.write(
                self.style.SUCCESS('Updated channel "%s"' % channel_obj.title))

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
                'tags': ", ".join(talk_data["snippet"]["tags"]),
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
