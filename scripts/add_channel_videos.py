#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Add all videos from a channel given its youtube URL.

Example:

    $ ./add_channel_videos.py https://www.youtube.com/channel/UC9ZNrGdT2aAdrNbX78lbNlQ

TODO:
- Channel created date should be the published date value from the API.
- Support channel description
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
- Support channel custom URLS
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
- Support channel thumbnails
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
- Support channel statistics (viewCount, subscriberCount)
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
"""

import os
import sys
import logging
import argparse

from urllib.parse import urlparse

import requests

from django.utils import timezone
from django.core.wsgi import get_wsgi_application

# TODO: Get the API key from an env variable/conf file/cli flag
YOUTUBE_API_KEY = "AIzaSyAdDZRxQSQ70JBqYXeMUGmHE1Z2evOVW4Q"
# TODO: Use relative path
PROJECT_PATH = "/Users/raul/Projects/vtalks/vtalks.net/web/"

def do_channel(data_json):
    """Create or update a channel.
    """
    from talks.models import Channel

    channel_obj, created = Channel.objects.update_or_create(
        code=data_json["id"],
        defaults={
            'code': data_json["id"],
            'title': data_json["snippet"]["title"],
            'updated': timezone.now(),
        },
    )
    if created:
        logging.info("created channel %s", channel_obj)
    else:
        logging.info("updated channel %s", channel_obj)

    return channel_obj


def fetch_data(channel_code):
    """Fetch channel data from Youtube API
    """
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    payload = {'id': channel_code,
               'part': 'snippet',
               'key': YOUTUBE_API_KEY}
    resp = requests.get(channel_url, params=payload)
    if resp.status_code != 200:
        logging.error(resp.status_code)
        exit(1)
    response_json = resp.json()
    data_json = response_json["items"][0]
    return data_json

def main():
    """Main entry point.

    Add all videos from a channel given its youtube URL.
    """
    # Configure logging level to INFO.
    logging.basicConfig(level=logging.INFO)

    # Setup CLI flags and arguments.
    parser = argparse.ArgumentParser(description='Add channel talks to the database.')
    parser.add_argument('url', type=str, help='a channel URL')

    # Parse CLI arguments.
    args = parser.parse_args()

    # Get the video code from the URL argument.
    path = urlparse(args.url).path
    channel_code = path.split('/')[-1]

    # Fetch channel
    data_json = fetch_data(channel_code)

    # Update or create channel
    channel_obj = do_channel(data_json)

if __name__ == '__main__':
    # Setup django environment & application.
    sys.path.append(PROJECT_PATH)
    os.chdir(PROJECT_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
    get_wsgi_application()

    main()
