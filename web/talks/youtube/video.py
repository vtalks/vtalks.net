import requests

from urllib.parse import urlsplit
from urllib.parse import parse_qs

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
               'part': 'snippet,contentDetails,statistics,topicDetails,status,recordingDetails,player,localizations,liveStreamingDetails',
               'key': youtube_api_key}
    resp = requests.get(video_url, params=payload)
    if resp.status_code != 200:
        raise CommandError('Error fetching video data "%s"' % resp.status_code)
    response_json = resp.json()
    video_data = None
    if len(response_json["items"]) > 0:
        video_data = response_json["items"][0]
    return video_data