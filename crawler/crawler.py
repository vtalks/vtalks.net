#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Youtube Video data crawler with Django environment loaded.

Example:

    $ ./crawler.py video https://www.youtube.com/watch?v=yeetIgNeIkc

FIXME:
- Video url should be on the model instead on the admin, also needs a better
  nanme.

TODO:
- Fetch video duration from contentDetails.
- Support channel custom URLS
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
- Support video thumbnails (readonly fields)
- Support channel statistics (viewCount, subscriberCount)
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
- Support channel playlists.
"""

import os
import sys
import logging
import argparse

from django.core.wsgi import get_wsgi_application

from youtube import utils
from youtube import video
from youtube import channel

# TODO: Get the API key from an env variable/conf file/cli flag 
YOUTUBE_API_KEY = "AIzaSyAdDZRxQSQ70JBqYXeMUGmHE1Z2evOVW4Q"
# TODO: Use relative path
PROJECT_PATH = "/Users/raul/Projects/vtalks/vtalks.net/web/"

def video_command(args):
    """Creates or updates a video and its channel given its URL.
    """
    # Fetch video data
    video_code = utils.get_code(args.url)
    video_data_json = video.fetch(YOUTUBE_API_KEY, video_code)
    # Fetch channel data
    channel_code = video_data_json["snippet"]["channelId"]
    channel_data_json = channel.fetch(YOUTUBE_API_KEY, channel_code)
    # Store channel and video
    channel_obj = channel.store(channel_data_json)
    video.store(video_data_json, channel_obj)

def channel_command(args):
    """Add a videos from a channel given its URL.
    """
    logging.info("channel")

def main():
    """Main entry point.
    """
    # Setup subcommands, flags and arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Enable verbose ouput", action="store_true")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    video_parser = subparsers.add_parser('video', help="Add video")
    video_parser.add_argument('url', type=str, help='a video URL')
    channel_parser = subparsers.add_parser('channel', help="Add channel videos")
    channel_parser.add_argument('url', type=str, help='a channel URL')
    args = parser.parse_args()

    if args.verbose:
        # Configure logging level to INFO.
        logging.basicConfig(level=logging.INFO)

    if args.command == "video":
        video_command(args)
        exit(0)

    if args.command == "channel":
        channel_command(args)
        exit(0)

if __name__ == '__main__':
    # Setup django environment & application.
    sys.path.append(PROJECT_PATH)
    os.chdir(PROJECT_PATH)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web.settings")
    get_wsgi_application()

    main()
