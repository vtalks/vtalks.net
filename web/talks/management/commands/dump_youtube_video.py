from django.conf import settings

from django.core.management.base import BaseCommand

from ...youtube.video import get_video_code
from ...youtube.video import fetch_video_data


class Command(BaseCommand):
    help = 'Dumps raw video data from Youtube API.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str)

    def fetch_video(self, youtube_url):
        video_code = get_video_code(youtube_url)

        talk_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        self.stdout.write(
            self.style.SUCCESS('Fetch talk "%s"' % talk_data["id"]))

        return talk_data

    def handle(self, *args, **options):
        talk_data = self.fetch_video(options['youtube_url'])
        self.stdout.write(str(talk_data))
