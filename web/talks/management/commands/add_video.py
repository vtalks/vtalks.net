import logging
import requests

from urllib.parse import urlsplit
from urllib.parse import parse_qs

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


def get_video_code(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    if "v" not in params:
        raise CommandError('Invalid url "%s"' % url)
    video_code = params["v"][0]
    return video_code


def fetch_video_data(youtube_api_key, video_code):
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    payload = {'id': video_code,
               'part': 'snippet,statistics',
               'key': youtube_api_key}
    resp = requests.get(video_url, params=payload)
    if resp.status_code != 200:
        logging.error(resp.status_code)
        exit(1)
    response_json = resp.json()
    video_data = response_json["items"][0]
    return video_data


class Command(BaseCommand):
    help = 'Adds a video to the system.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str)

    def handle(self, *args, **options):
        video_code = get_video_code(options['youtube_url'])
        video_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)
        dir(video_data)
