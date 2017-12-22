#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Youtube Video data crawler with Django environment loaded.

Example:

    $ ./crawler.py video https://www.youtube.com/watch?v=yeetIgNeIkc

TODO:
- Fetch video duration from contentDetails.
- Support channel custom URLS
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
- Support channel statistics (viewCount, subscriberCount)
  (see API docs https://developers.google.com/youtube/v3/docs/channels/list)
"""

import os
import sys
import logging
import argparse

from django.core.wsgi import get_wsgi_application

from .youtube import utils
from .youtube import video
from .youtube import channel
from .youtube import playlist

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')


def video_command(args):
    # Fetch video data
    video_code = utils.get_video_code(args.url)
    video_data_json = video.fetch(YOUTUBE_API_KEY, video_code)
    # Fetch channel data
    channel_code = video_data_json["snippet"]["channelId"]
    channel_data_json = channel.fetch(YOUTUBE_API_KEY, channel_code)
    # Store channel and video
    channel_obj = channel.store(channel_data_json)
    video.store(video_data_json, channel_obj)


def channel_command(args):
    # Fetch channel data
    channel_code = utils.get_channel_code(args.url)
    channel_data_json = channel.fetch(YOUTUBE_API_KEY, channel_code)
    # Fetch uploads list id
    channel_upload_list_id = channel_data_json["contentDetails"]["relatedPlaylists"]["uploads"]
    # Fetch uploads list videos
    # TODO:
    # - Support pagination
    channel_videos_ids = playlist.fetch_items(YOUTUBE_API_KEY,
                                              channel_upload_list_id)
    # Store channel and video
    channel_obj = channel.store(channel_data_json)
    for item in channel_videos_ids:
        video_data_json = video.fetch(YOUTUBE_API_KEY, item)
        video.store(video_data_json, channel_obj)


def main():
    # Setup sub commands, flags and arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", help="Enable verbose ouput",
                        action="store_true")
    subparsers = parser.add_subparsers(dest='command')
    subparsers.required = True
    video_parser = subparsers.add_parser('video', help="Add video")
    video_parser.add_argument('url', type=str, help='a video URL')
    channel_parser = subparsers.add_parser('channel', help="Add channel videos")
    channel_parser.add_argument('url', type=str, help='a channel URL')
    args = parser.parse_args()

    if args.verbose:
        # Configure logging level to INFO.
        logging.basicConfig(level=logging.INFO)

    if args.command == "video":
        video_command(args)
        exit(0)

    if args.command == "channel":
        channel_command(args)
        exit(0)


if __name__ == '__main__':
    # Add crawler and web to the python path
    crawler_path = os.getcwd()
    web_path = os.path.normpath(os.path.join(crawler_path, "../web/"))
    sys.path.append(crawler_path)
    sys.path.append(web_path)

    # Setup django environment & application.
    os.chdir(web_path)
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")
    get_wsgi_application()

    # Execute main entry point
    main()
