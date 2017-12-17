#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add a talk and a channel given a youtube URL.

Example:

    $ ./add_video.py https://www.youtube.com/watch?v=yeetIgNeIkc

TODO:
- Fetch duration from contentDetails.
- Channel created date should be the published date value from the API.
"""

import os
import sys
import logging
import argparse

from urllib.parse import urlsplit, parse_qs

import requests

from django.utils import timezone
from django.core.wsgi import get_wsgi_application

# TODO: Get the API key from an env variable/conf file/cli flag 
YOUTUBE_API_KEY = "AIzaSyAdDZRxQSQ70JBqYXeMUGmHE1Z2evOVW4Q"
# TODO: Use relative path
PROJECT_PATH = "/Users/raul/Projects/vtalks/vtalks.net/web/"

def do_channel(data_json):
    """Create or update a channel.

    Returns the channel object from the database.
    """
    from talks.models import Channel

    channel_obj, created = Channel.objects.update_or_create(
        code=data_json["snippet"]["channelId"],
        defaults={
            'code': data_json["snippet"]["channelId"],
            'title': data_json["snippet"]["channelTitle"],
            'updated': timezone.now(),
        },
    )
    if created:
        logging.info("created channel %s", channel_obj)
    else:
        logging.info("updated channel %s", channel_obj)

    return channel_obj

def do_talk(data_json, channel_obj):
    """Create or update talk.
    """
    from talks.models import Talk

    if "tags" not in data_json["snippet"]:
        data_json["snippet"]["tags"] = []
    if "likeCount" not in data_json["statistics"]:
        data_json["statistics"]["likeCount"] = 0
    if "dislikeCount" not in data_json["statistics"]:
        data_json["statistics"]["dislikeCount"] = 0
    video_obj, created = Talk.objects.update_or_create(
        code=data_json["id"],
        defaults={
            'code': data_json["id"],
            'title': data_json["snippet"]["title"],
            'description': data_json["snippet"]["description"],
            'channel': channel_obj,
            'viewCount': data_json["statistics"]["viewCount"],
            'likeCount': data_json["statistics"]["likeCount"],
            'dislikeCount': data_json["statistics"]["dislikeCount"],
            'tags': ", ".join(data_json["snippet"]["tags"]),
            'created': data_json["snippet"]["publishedAt"],
            'updated': timezone.now(),
        },
    )
    if created:
        logging.info("created talk %s", video_obj)
    else:
        logging.info("updated talk %s", video_obj)

def fetch_data(video_code):
    """Fetch video data from Youtube API
    """
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    payload = {'id': video_code,
               'part': 'snippet,statistics',
               'key': YOUTUBE_API_KEY}
    resp = requests.get(video_url, params=payload)
    if resp.status_code != 200:
        logging.error(resp.status_code)
        exit(1)
    response_json = resp.json()
    data_json = response_json["items"][0]
    return data_json

def main():
    """Main entry point.

    Add a talk and a channel given a youtube URL.
    """
    # Configure logging level to INFO.
    logging.basicConfig(level=logging.INFO)

    # Setup CLI flags and arguments.
    parser = argparse.ArgumentParser(description='Add talk to the database.')
    parser.add_argument('url', type=str, help='a video URL')

    # Parse CLI arguments.
    args = parser.parse_args()

    # Get the video code from the URL argument.
    query = urlsplit(args.url).query
    params = parse_qs(query)
    if "v" not in params:
        logging.error("Invalid url %s", args.url)
        exit(1)
    video_code = params["v"][0]

    # Fetch video
    data_json = fetch_data(video_code)

    # Update or create channel
    channel_obj = do_channel(data_json)

    # Update or create talk
    do_talk(data_json, channel_obj)

if __name__ == '__main__':
    # Setup django environment & application.
    sys.path.append(PROJECT_PATH)
    os.chdir(PROJECT_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
    get_wsgi_application()

    main()
