import requests

from django.core.management.base import CommandError


def fetch_channel_data(youtube_api_key, channel_code):
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    payload = {'id': channel_code,
               'part': 'snippet,contentDetails',
               'key': youtube_api_key}
    resp = requests.get(channel_url, params=payload)
    if resp.status_code != 200:
        raise CommandError('Error fetching channel data "%s"' % resp.status_code)
    response_json = resp.json()
    channel_data = None
    if len(response_json["items"]) > 0:
        channel_data = response_json["items"][0]
    return channel_data
