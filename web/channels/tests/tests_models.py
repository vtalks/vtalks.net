from django.test import TestCase

from channels.models import Channel

# Create your tests here.


class ChannelModelTests(TestCase):

    def setUp(self):
        Channel.objects.create(code='1', title='channel title 1')

    def test_instance_get_string_repr(self):
        """ Channel object string representation returns its title
        """
        channel_1 = Channel.objects.get(code='1')
        self.assertEquals(str(channel_1), channel_1.title)

    def test_instance_get_youtube_valid_url(self):
        """All Channel models have a property that returns the external
        youtube url.
        """
        channel_1 = Channel.objects.get(code='1')
        self.assertEquals(channel_1.youtube_url, 'https://www.youtube.com/channel/1')