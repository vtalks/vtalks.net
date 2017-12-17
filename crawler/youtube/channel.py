# -*- coding: utf-8 -*-
"""Youtube API Client
"""
import logging

import requests

from django.utils import timezone

def fetch(youtube_api_key, channel_code):
    """Fetch channel data from Youtube API
    """
    channel_url = "https://www.googleapis.com/youtube/v3/channels"
    payload = {'id': channel_code,
               'part': 'snippet',
               'key': youtube_api_key}
    resp = requests.get(channel_url, params=payload)
    if resp.status_code != 200:
        logging.error(resp.status_code)
        exit(1)
    response_json = resp.json()
    print(resp.text)
    data_json = response_json["items"][0]
    return data_json

def store(channel_data_json):
    """Create or update video channel
    """
    from talks.models import Channel

    channel_obj, created = Channel.objects.update_or_create(
        code=channel_data_json["id"],
        defaults={
            'code': channel_data_json["id"],
            'title': channel_data_json["snippet"]["title"],
            'description': channel_data_json["snippet"]["description"],
            'created': channel_data_json["snippet"]["publishedAt"],
            'updated': timezone.now(),
        },
    )
    if created:
        logging.info("created channel %s", channel_obj)
    else:
        logging.info("updated channel %s", channel_obj)

    return channel_obj
