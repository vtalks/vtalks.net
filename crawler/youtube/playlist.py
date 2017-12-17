# -*- coding: utf-8 -*-
"""Youtube API Client
"""
import logging

import requests

def fetch_items(youtube_api_key, playlist_code):
    """Fetch playlist data from Youtube API
    """
    channel_url = "https://www.googleapis.com/youtube/v3/playlistItems"
    payload = {'playlistId': playlist_code,
               'maxResults': 50,
               'part': 'snippet',
               'key': youtube_api_key}
    resp = requests.get(channel_url, params=payload)
    if resp.status_code != 200:
        logging.error(resp.status_code)
        exit(1)
    response_json = resp.json()
    data_json = response_json["items"]
    videos_id_list = []
    for item in data_json:
        videos_id_list.append(item["snippet"]["resourceId"]["videoId"])
    return videos_id_list
