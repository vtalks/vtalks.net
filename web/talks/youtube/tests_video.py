from django.test import TestCase
from django.core.management.base import CommandError

from .video import get_video_code

# Create your tests here.


class YoutubeVideoTests(TestCase):

    def test_get_video_code(self):
        url = 'https://www.youtube.com/watch?v=code'
        video_code = get_video_code(url)
        self.assertEquals(video_code, 'code')

    def test_get_video_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_video_code, url)
