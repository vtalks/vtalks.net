from urllib.parse import urlsplit
from urllib.parse import parse_qs

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


def get_playlist_code(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    if "list" not in params:
        raise CommandError('Invalid url "%s"' % url)
    playlist_code = params["list"][0]
    return playlist_code


class Command(BaseCommand):
    help = 'Adds a video playlist to the system.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str)

    def handle(self, *args, **options):
        playlist_code = get_playlist_code(options['youtube_url'])
        print(playlist_code)
