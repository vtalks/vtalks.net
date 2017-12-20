# -*- coding: utf-8 -*-
import logging

from urllib.parse import urlparse
from urllib.parse import urlsplit
from urllib.parse import parse_qs


def get_video_code(url):
    query = urlsplit(url).query
    params = parse_qs(query)
    if "v" not in params:
        logging.error("Invalid url %s", url)
        exit(1)
    video_code = params["v"][0]
    return video_code


def get_channel_code(url):
    path = urlparse(url).path
    channel_code = path.split('/')[-1]
    return channel_code
