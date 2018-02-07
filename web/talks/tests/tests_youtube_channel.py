import requests_mock

from django.conf import settings
from django.test import TestCase
from django.core.management.base import CommandError

from talks.youtube.channel import get_channel_code
from talks.youtube.channel import fetch_channel_data

# Create your tests here.


class YoutubeChannelTests(TestCase):

    def test_get_channel_code(self):
        url = 'https://www.youtube.com/channel/code'
        channel_code = get_channel_code(url)
        self.assertEquals(channel_code, 'code')

    def test_get_channel_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_channel_code, url)

    def test_fetch_channel_data_fails_invalid_youtube_key(self):
        url='https://www.googleapis.com/youtube/v3/channels'
        with requests_mock.mock() as m:
            m.get(url, json={}, status_code=400)
            youtube_api_key = 'invalid_youtube_key'
            channel_code = 'code'
            self.assertRaises(CommandError, fetch_channel_data, youtube_api_key, channel_code)

    def test_fetch_channel_data_fails_code_not_found(self):
        url = 'https://www.googleapis.com/youtube/v3/channels'
        with requests_mock.mock() as m:
            m.get(url, json={"items": []}, status_code=200)
            youtube_api_key = settings.YOUTUBE_API_KEY
            channel_code = 'invalid_code'
            channel_data = fetch_channel_data(youtube_api_key, channel_code)
            self.assertIsNone(channel_data)

    def test_fetch_channel_data(self):
        url = 'https://www.googleapis.com/youtube/v3/channels'
        with requests_mock.mock() as m:
            m.get(url, json={"items": [{"id": 'code'}]}, status_code=200)
            youtube_api_key = settings.YOUTUBE_API_KEY
            channel_code = 'code'
            channel_data = fetch_channel_data(youtube_api_key, channel_code)
            self.assertEquals(channel_data['id'], channel_code)