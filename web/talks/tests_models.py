import requests_mock

from django.test import TestCase
from django.conf import settings
from django.core.management.base import CommandError

from .models import Channel
from .models import fetch_channel_data
from .models import fetch_video_data
from .models import Talk

# Create your tests here.


class ChannelModelTests(TestCase):

    def setUp(self):
        Channel.objects.create(code='1', title='channel title 1')

    def test_instance_get_string_repr(self):
        """Channel object string representation returns its title"""
        channel_1 = Channel.objects.get(code='1')
        self.assertEquals(str(channel_1), channel_1.title)

    def test_instance_get_youtube_valid_url(self):
        """All Channel models have a property that returns the external
        youtube url.
        """
        channel_1 = Channel.objects.get(code='1')
        self.assertEquals(channel_1.youtube_url, 'https://www.youtube.com/channel/1')


class TalkModelTests(TestCase):

    def setUp(self):
        chanel_1 = Channel.objects.create(code='1', title='channel title 1')
        Talk.objects.create(code='1', title='talk title 1', channel=chanel_1)
        Talk.objects.create(code='11', title='talk title same title', channel=chanel_1)
        Talk.objects.create(code='12', title='talk title same title', channel=chanel_1)

    def test_instance_get_string_repr(self):
        """Talk object string representation returns its title"""
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(str(talk_1), talk_1.title)

    def test_instance_get_youtube_valid_url(self):
        """All Talk models have a property that returns the external youtube
        url.
        """
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(talk_1.youtube_url,
                          'https://www.youtube.com/watch?v=1')

    def test_instance_thumbnails(self):
        """A talk have a set of thumbnails of different resolutions based on
        its code.
        """
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(talk_1.default_thumb,
                          'https://i.ytimg.com/vi/1/default.jpg')
        self.assertEquals(talk_1.medium_thumb,
                          'https://i.ytimg.com/vi/1/mqdefault.jpg')
        self.assertEquals(talk_1.high_thumb,
                          'https://i.ytimg.com/vi/1/hqdefault.jpg')
        self.assertEquals(talk_1.standard_thumb,
                          'https://i.ytimg.com/vi/1/sddefault.jpg')
        self.assertEquals(talk_1.maxres_thumb,
                          'https://i.ytimg.com/vi/1/maxresdefault.jpg')

    def test_instance_slug(self):
        """A talk populates automatically an slug field once it is created"""
        talk_1 = Talk.objects.get(code='1')
        self.assertEquals(talk_1.slug, 'talk-title-1')

    def test_duplicate_title_slug(self):
        """It is possible than two different talks have the same title, in
        this case the slug will have the talk code as a suffix on the second
        talk.
        """
        talk_12 = Talk.objects.get(code='12')
        self.assertEquals(talk_12.slug, 'talk-title-same-title-12')


class FetchYoutubeChannelTests(TestCase):
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


class FetchYoutubeVideoTests(TestCase):
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
