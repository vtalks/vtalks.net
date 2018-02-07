import requests_mock

from django.conf import settings
from django.test import TestCase
from django.core.management.base import CommandError

from talks.youtube.playlist import get_playlist_code
from talks.youtube.playlist import fetch_playlist_items

# Create your tests here.


class YoutubePlaylistTests(TestCase):

    def test_get_playlist_code(self):
        url = 'https://www.youtube.com/playlist?list=code'
        playlist_code = get_playlist_code(url)
        self.assertEquals(playlist_code, 'code')

    def test_get_playlist_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_playlist_code, url)

    def test_fetch_playlist_data_fails_invalid_youtube_key(self):
        url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        with requests_mock.mock() as m:
            m.get(url, json={}, status_code=400)
            youtube_api_key = 'invalid_youtube_key'
            playlist_code = 'code'
            self.assertRaises(CommandError, fetch_playlist_items, youtube_api_key, playlist_code)

    def test_fetch_playlist_data_fails_code_not_found(self):
        url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        with requests_mock.mock() as m:
            m.get(url, json={"code": 404, "message": "The playlist identified with the requests playlistId parameter cannot be found."}, status_code=404)
            youtube_api_key = settings.YOUTUBE_API_KEY
            playlist_code = 'invalid_code'
            playlist_data = fetch_playlist_items(youtube_api_key, playlist_code)
            self.assertIsInstance(playlist_data, list)
            self.assertEquals(len(playlist_data), 0)

    def test_fetch_playlist_data(self):
        url = 'https://www.googleapis.com/youtube/v3/playlistItems'
        with requests_mock.mock() as m:
            m.get(url, json={"items": [{"snippet": {"resourceId": {"videoId": "1"}}}, {"snippet": {"resourceId": {"videoId": "2"}}}]}, status_code=200)
            youtube_api_key = settings.YOUTUBE_API_KEY
            playlist_code = 'UC_x5XG1OV2P6uZZ5FSM9Ttw'
            playlist_data = fetch_playlist_items(youtube_api_key, playlist_code)
            self.assertIsInstance(playlist_data, list)