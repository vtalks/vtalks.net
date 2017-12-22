from unittest import mock
from io import StringIO
from django.test import TestCase
from django.core.management import call_command
from django.core.management.base import CommandError

from .management.commands.add_video import get_video_code
from .management.commands.add_playlist import get_playlist_code

# Create your tests here.


class AddVideoCommandTests(TestCase):

    def test_get_video_code(self):
        url = 'https://www.youtube.com/watch?v=code'
        video_code = get_video_code(url)
        self.assertEquals(video_code, 'code')

    def test_get_video_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_video_code, url)

    '''
    def fake_fetch_video_data(self, youtube_api_key, video_code):
        return {'snippet': {'channelId': '1'}}

    @mock.patch('talks.models.fetch_video_data', fake_fetch_video_data)
    def test_command_output(self):
        out = StringIO()
        call_command('add_video', 'https://www.youtube.com/watch?v=code', stdout=out)
        self.assertIn('Expected output', out.getvalue())
    '''


class AddPlaylistCommandTests(TestCase):

    def test_get_playlist_code(self):
        url = 'https://www.youtube.com/playlist?list=code'
        playlist_code = get_playlist_code(url)
        self.assertEquals(playlist_code, 'code')

    def test_get_playlist_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_playlist_code, url)
