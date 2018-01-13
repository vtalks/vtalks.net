import re

from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.management.base import BaseCommand

from ...models import Channel
from ...models import Talk
from ...youtube.channel import fetch_channel_data
from ...youtube.video import get_video_code
from ...youtube.video import fetch_video_data

"""
TODO:

#### Open questions

* Support video favoriteCount
* Support channel custom URLS
* Support channel statistics (viewCount, subscriberCount)

## Additional information

https://developers.google.com/youtube/v3/docs/channels/list
"""


class Command(BaseCommand):
    help = 'Adds a video to the system.'

    def add_arguments(self, parser):
        pass

    def update_video(self, youtube_url):
        video_code = get_video_code(youtube_url)
        talk_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        self.stdout.write(
            self.style.SUCCESS('Adding talk "%s"' % talk_data["id"]))

        channel_code = talk_data["snippet"]["channelId"]
        channel_data = fetch_channel_data(settings.YOUTUBE_API_KEY,
                                          channel_code)

        self.stdout.write(
            self.style.SUCCESS('Adding channel "%s"' % channel_data["id"]))

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
            self.stdout.write('Added channel "%s"' % channel_obj.title)
        else:
            self.stdout.write('Updated channel "%s"' % channel_obj.title)

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
            self.stdout.write('Added talk "%s"' % talk_obj.title)
        else:
            self.stdout.write('Updated talk "%s"' % talk_obj.title)

        talk_obj = Talk.objects.get(code=talk_data["id"])

        # Add tags from cli arguments and talk_data
        video_tags = [] # options['tags']
        if "tags" in talk_data["snippet"]:
            video_tags += talk_data["snippet"]["tags"]
        for tag in video_tags:
            talk_obj.tags.add(tag)
            self.stdout.write('Tagged as "%s"' % tag)

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

        d = timedelta(hours=int(hours), minutes=int(minutes), seconds=int(seconds))
        talk_obj.duration = d

        talk_obj.save()

    def handle(self, *args, **options):
        talks = Talk.objects.all().order_by('updated')
        for talk in talks:
            self.update_video(talk.youtube_url)