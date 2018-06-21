from unittest.mock import patch

from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command

# Create your tests here.


class AddPlayListCommandTests(TestCase):

    @patch("playlists.management.commands.add_playlist.fetch_channel_data")
    @patch("playlists.management.commands.add_playlist.fetch_video_data")
    @patch("playlists.management.commands.add_playlist.fetch_playlist_data")
    @patch("playlists.management.commands.add_playlist.fetch_playlist_items")
    def test_command(self, fake_fetch_playlist_items, fake_fetch_playlist_data, fake_fetch_video_data, fake_fetch_channel_data):
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
            },
            "contentDetails": {
                "duration": "PT1H46M12S",
            },
        }
        # mock fetch channel data
        fake_fetch_channel_data.return_value = {
            "id": "fake_channel_id",
            "snippet": {
                "title": "channel title",
                "description": "channel description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            },
            "contentDetails": {
                "duration": "PT1H46M12S",
            },
        }
        # mock fetch playlist data
        fake_fetch_playlist_data.return_value = {
            "id": "fake_playlist_id",
            "snippet": {
                "title": "playlist title",
                "description": "playlist description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            }
        }

        out = StringIO()
        call_command('add_playlist', 'https://www.youtube.com/playlist?list=list_code', verbosity=1, stdout=out)
        output = out.getvalue()
        # self.assertIn('Created channel successfully', output)
        # self.assertIn('Added talk "video title"', output)
