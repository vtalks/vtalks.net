from django.test import TestCase
from django.core.management.base import CommandError

from .playlist import get_playlist_code

# Create your tests here.


class YoutubePlaylistTests(TestCase):

    def test_get_playlist_code(self):
        url = 'https://www.youtube.com/playlist?list=code'
        playlist_code = get_playlist_code(url)
        self.assertEquals(playlist_code, 'code')

    def test_get_playlist_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_playlist_code, url)
