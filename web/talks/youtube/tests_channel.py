from django.test import TestCase
from django.core.management.base import CommandError

from .channel import get_channel_code

# Create your tests here.


class YoutubeChannelTests(TestCase):

    def test_get_channel_code(self):
        url = 'https://www.youtube.com/channel/code'
        channel_code = get_channel_code(url)
        self.assertEquals(channel_code, 'code')

    def test_get_channel_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_channel_code, url)
