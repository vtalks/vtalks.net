# -*- coding: utf-8 -*-
import logging

import requests

from django.utils import timezone


def fetch(youtube_api_key, video_code):
    video_url = "https://www.googleapis.com/youtube/v3/videos"
    payload = {'id': video_code,
               'part': 'snippet,statistics',
               'key': youtube_api_key}
    resp = requests.get(video_url, params=payload)
    if resp.status_code != 200:
        logging.error(resp.status_code)
        exit(1)
    response_json = resp.json()
    data_json = response_json["items"][0]
    return data_json


def store(video_data_json, channel_obj):
    from talks.models import Talk

    if "tags" not in video_data_json["snippet"]:
        video_data_json["snippet"]["tags"] = []
    if "likeCount" not in video_data_json["statistics"]:
        video_data_json["statistics"]["likeCount"] = 0
    if "dislikeCount" not in video_data_json["statistics"]:
        video_data_json["statistics"]["dislikeCount"] = 0
    
    video_obj, created = Talk.objects.update_or_create(
        code=video_data_json["id"],
        defaults={
            'code': video_data_json["id"],
            'title': video_data_json["snippet"]["title"],
            'description': video_data_json["snippet"]["description"],
            'channel': channel_obj,
            'viewCount': video_data_json["statistics"]["viewCount"],
            'likeCount': video_data_json["statistics"]["likeCount"],
            'dislikeCount': video_data_json["statistics"]["dislikeCount"],
            'tags': ", ".join(video_data_json["snippet"]["tags"]),
            'created': video_data_json["snippet"]["publishedAt"],
            'updated': timezone.now(),
        },
    )
    if created:
        logging.info("created talk %s", video_obj)
    else:
        logging.info("updated talk %s", video_obj)

    return video_obj
