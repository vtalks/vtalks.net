from django.test import TestCase

from .management.commands.add_video import get_video_code
from .management.commands.add_playlist import get_playlist_code

# Create your tests here.


class AddVideoCommandTests(TestCase):

    def test_get_video_code(self):
        url = 'https://www.youtube.com/watch?v=code'
        video_code = get_video_code(url)
        self.assertEquals(video_code, 'code')


class AddPlaylistCommandTests(TestCase):

    def test_get_playlist_code(self):
        url = 'https://www.youtube.com/playlist?list=code'
        playlist_code = get_playlist_code(url)
        self.assertEquals(playlist_code, 'code')
