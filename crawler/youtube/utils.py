# -*- coding: utf-8 -*-
"""Common URL utils
"""
import logging

from urllib.parse import urlsplit
from urllib.parse import parse_qs

def get_code(url):
    """Get the video code from the URL argument.
    """
    query = urlsplit(url).query
    params = parse_qs(query)
    if "v" not in params:
        logging.error("Invalid url %s", url)
        exit(1)
    video_code = params["v"][0]
    return video_code
