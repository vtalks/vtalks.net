#!/usr/bin/env python3
"""Add a talk and a channel given a youtube URL.

Example:

    $ ./add_video.py https://www.youtube.com/watch?v=yeetIgNeIkc
"""

import os
import sys
import logging
import argparse

from urllib.parse import urlsplit, parse_qs

import requests

from django.utils import timezone
from django.core.wsgi import get_wsgi_application

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

    # TODO: Use relative path
    project_path = "/Users/raul/Projects/vtalks/vtalks.net/web/"

    # This is so my local_settings.py gets loaded.
    sys.path.append(project_path)
    os.chdir(project_path)

    # This is so Django knows where to find stuff.
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")

    # This is so models get loaded.
    get_wsgi_application()

    # Fetch video
    youtube_api_key = "AIzaSyAdDZRxQSQ70JBqYXeMUGmHE1Z2evOVW4Q"

    video_url = "https://www.googleapis.com/youtube/v3/videos"
    payload = {'id': video_code,
               'part': 'snippet,statistics',
               'key': youtube_api_key}
    resp = requests.get(video_url, params=payload)
    if resp.status_code != 200:
        logging.error(resp.status_code)
        exit(1)

    response_json = resp.json()

    video_json = response_json["items"][0]

    from talks.models import Channel
    from talks.models import Talk

    # Update or create channel
    channel_obj, created = Channel.objects.update_or_create(
        code=video_json["snippet"]["channelId"],
        defaults={
            'code': video_json["snippet"]["channelId"],
            'title': video_json["snippet"]["channelTitle"],
            'updated': timezone.now(),
        },
    )
    if created:
        logging.info("created channel %s", channel_obj)
    else:
        logging.info("updated channel %s", channel_obj)

    # Update or create talk
    if "tags" not in video_json["snippet"]:
        video_json["snippet"]["tags"] = []
    video_obj, created = Talk.objects.update_or_create(
        code=video_json["id"],
        defaults={
            'code': video_json["id"],
            'title': video_json["snippet"]["title"],
            'description': video_json["snippet"]["description"],
            'channel': channel_obj,
            'viewCount': video_json["statistics"]["viewCount"],
            'likeCount': video_json["statistics"]["likeCount"],
            'dislikeCount': video_json["statistics"]["dislikeCount"],
            'tags': ", ".join(video_json["snippet"]["tags"]),
            'updated': timezone.now(),
        },
    )
    if created:
        logging.info("created talk %s", video_obj)
    else:
        logging.info("updated talk %s", video_obj)

if __name__ == '__main__':
    main()
