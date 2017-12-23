
from unittest.mock import patch

from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command
from django.core.management.base import CommandError

from .management.commands.add_video import get_video_code
from .management.commands.add_playlist import get_playlist_code


# Create your tests here.


class AddVideoCommandUtilsTests(TestCase):

    def test_get_video_code(self):
        url = 'https://www.youtube.com/watch?v=code'
        video_code = get_video_code(url)
        self.assertEquals(video_code, 'code')

    def test_get_video_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_video_code, url)


class AddPlaylistCommandTests(TestCase):

    def test_get_playlist_code(self):
        url = 'https://www.youtube.com/playlist?list=code'
        playlist_code = get_playlist_code(url)
        self.assertEquals(playlist_code, 'code')

    def test_get_playlist_code_fails(self):
        url = 'invalid_url'
        self.assertRaises(CommandError, get_playlist_code, url)


class AddVideoCommandTests(TestCase):

    @patch("talks.management.commands.add_video.fetch_video_data")
    @patch("talks.management.commands.add_video.fetch_channel_data")
    def test_command(self, fake_fetch_channel_data, fake_fetch_video_data):
        # mock fetch video data
        fake_fetch_video_data.return_value = {
            "id": "fake_video_id",
            "snippet": {
                "channelId": "fake_channel_id",
                "title": "video title",
                "description": "video description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            },
            "statistics": {
                "viewCount": 20,
            }
        }
        # mock fetch channel data
        fake_fetch_channel_data.return_value = {
            "id": "fake_channel_id",
            "snippet": {
                "title": "channel title",
                "description": "channel description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            }
        }

        out = StringIO()
        call_command('add_video', 'https://www.youtube.com/watch?v=video_code', stdout=out)
        output = out.getvalue()
        self.assertIn('Adding talk "fake_video_id"', output)
        self.assertIn('Adding channel "fake_channel_id"', output)
        self.assertIn('Added channel "channel title"', output)
        self.assertIn('Added talk "video title"', output)

        # mock fetch video data
        fake_fetch_video_data.return_value = {
            "id": "fake_video_id",
            "snippet": {
                "channelId": "fake_channel_id",
                "title": "updated video title",
                "description": "video description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
                "tags": "tag1, tag2",
            },
            "statistics": {
                "viewCount": 20,
                "likeCount": 10,
                "dislikeCount": 5,
            }
        }
        # mock fetch channel data
        fake_fetch_channel_data.return_value = {
            "id": "fake_channel_id",
            "snippet": {
                "title": "updated channel title",
                "description": "channel description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            }
        }

        out = StringIO()
        call_command('add_video', 'https://www.youtube.com/watch?v=video_code',
                     stdout=out)
        output = out.getvalue()
        self.assertIn('Adding talk "fake_video_id"', output)
        self.assertIn('Adding channel "fake_channel_id"', output)
        self.assertIn('Updated channel "updated channel title"', output)
        self.assertIn('Updated talk "updated video title"', output)


class AddPlayListCommandTests(TestCase):

    @patch("talks.management.commands.add_playlist.fetch_channel_data")
    @patch("talks.management.commands.add_playlist.fetch_video_data")
    @patch("talks.management.commands.add_playlist.fetch_playlist_items")
    def test_command(self, fake_fetch_playlist_items, fake_fetch_video_data, fake_fetch_channel_data):
        # mock fetch playlist items
        fake_fetch_playlist_items.return_value = ['fake_video_id']
        # mock fetch video data
        fake_fetch_video_data.return_value = {
            "id": "fake_video_id",
            "snippet": {
                "channelId": "fake_channel_id",
                "title": "video title",
                "description": "video description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            },
            "statistics": {
                "viewCount": 20,
            }
        }
        # mock fetch channel data
        fake_fetch_channel_data.return_value = {
            "id": "fake_channel_id",
            "snippet": {
                "title": "channel title",
                "description": "channel description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            }
        }

        out = StringIO()
        call_command('add_playlist', 'https://www.youtube.com/playlist?list=list_code', stdout=out)
        output = out.getvalue()
        self.assertIn('Added channel "channel title"', output)
        self.assertIn('Added talk "video title"', output)

        # mock fetch video data
        fake_fetch_video_data.return_value = {
            "id": "fake_video_id",
            "snippet": {
                "channelId": "fake_channel_id",
                "title": "updated video title",
                "description": "video description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
                "tags": "tag1, tag2",
            },
            "statistics": {
                "viewCount": 20,
                "likeCount": 10,
                "dislikeCount": 5,
            }
        }
        # mock fetch channel data
        fake_fetch_channel_data.return_value = {
            "id": "fake_channel_id",
            "snippet": {
                "title": "updated channel title",
                "description": "channel description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            }
        }

        out = StringIO()
        call_command('add_playlist',
                     'https://www.youtube.com/playlist?list=list_code',
                     stdout=out)
        output = out.getvalue()
        self.assertIn('Updated channel "updated channel title"', output)
        self.assertIn('Updated talk "updated video title"', output)
