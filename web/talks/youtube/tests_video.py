import requests_mock

from django.conf import settings
from django.test import TestCase
from django.core.management.base import CommandError

from .video import get_video_code
from .video import fetch_video_data

# Create your tests here.


class YoutubeVideoTests(TestCase):

    def test_get_video_code(self):
        url = 'https://www.youtube.com/watch?v=code'
        video_code = get_video_code(url)
        self.assertEquals(video_code, 'code')

    def test_get_video_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_video_code, url)

    def test_fetch_video_data_fails_invalid_youtube_key(self):
        url='https://www.googleapis.com/youtube/v3/videos'
        with requests_mock.mock() as m:
            m.get(url, json={}, status_code=400)
            youtube_api_key = 'invalid_youtube_key'
            video_code = 'code'
            self.assertRaises(CommandError, fetch_video_data, youtube_api_key, video_code)

    def test_fetch_video_data_fails_code_not_found(self):
        url = 'https://www.googleapis.com/youtube/v3/videos'
        with requests_mock.mock() as m:
            m.get(url, json={"items": []}, status_code=200)
            youtube_api_key = settings.YOUTUBE_API_KEY
            video_code = 'invalid_code'
            video_data = fetch_video_data(youtube_api_key, video_code)
            self.assertIsNone(video_data)

    def test_fetch_video_data(self):
        url = 'https://www.googleapis.com/youtube/v3/videos'
        with requests_mock.mock() as m:
            m.get(url, json={"items": [{"id": 'code'}]}, status_code=200)
            youtube_api_key = settings.YOUTUBE_API_KEY
            video_code = 'code'
            video_data = fetch_video_data(youtube_api_key, video_code)
            self.assertEquals(video_data['id'], video_code)
