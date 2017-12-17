# -*- coding: utf-8 -*-
"""Common URL utils
"""
import logging

from urllib.parse import urlparse
from urllib.parse import urlsplit
from urllib.parse import parse_qs

def get_video_code(url):
    """Get the video code from the URL argument.
    """
    query = urlsplit(url).query
    params = parse_qs(query)
    if "v" not in params:
        logging.error("Invalid url %s", url)
        exit(1)
    video_code = params["v"][0]
    return video_code

def get_channel_code(url):
    """Get the channel code from the URL argument.
    """
    path = urlparse(url).path
    channel_code = path.split('/')[-1]
    return channel_code
