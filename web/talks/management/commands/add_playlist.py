import requests

from urllib.parse import urlsplit
from urllib.parse import parse_qs

from django.conf import settings
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

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


def fetch_playlist_items(youtube_api_key, playlist_code):
    channel_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    payload = {'playlistId': playlist_code,
               'maxResults': 50,
               'part': 'snippet',
               'key': youtube_api_key}
    resp = requests.get(channel_url, params=payload)
    if resp.status_code != 200:
        raise CommandError('Error fetching playlist items "%s"' % resp.status_code)
    response_json = resp.json()
    data_json = response_json["items"]
    videos_id_list = []
    for item in data_json:
        videos_id_list.append(item["snippet"]["resourceId"]["videoId"])
    return videos_id_list


class Command(BaseCommand):
    help = 'Adds all videos from a playlist to the system.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', type=str)

    def handle(self, *args, **options):
        playlist_code = get_playlist_code(options['youtube_url'])
        playlist_videos = fetch_playlist_items(settings.YOUTUBE_API_KEY, playlist_code)
        for video_code in playlist_videos:
            print(video_code)
