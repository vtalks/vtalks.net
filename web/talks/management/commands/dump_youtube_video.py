import pprint

from django.conf import settings

from django.core.management.base import BaseCommand

from ...models import get_video_code
from ...models import fetch_video_data


class Command(BaseCommand):
    help = 'Dumps raw video data from Youtuge API.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str)

    def handle(self, *args, **options):
        video_code = get_video_code(options['youtube_url'])
        talk_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        pp = pprint.PrettyPrinter(indent=4, width=120)
        pp.pprint(talk_data)