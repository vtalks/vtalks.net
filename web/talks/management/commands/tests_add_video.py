from unittest.mock import patch

from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command

# Create your tests here.


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
            "contentDetails": {
                "duration": "PT1H46M12S",
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
            },
            "contentDetails": {
                "duration": "PT1H46M12S",
            },
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
            },
            "contentDetails": {
                "duration": "PT1H46M12S",
            },
        }
        # mock fetch channel data
        fake_fetch_channel_data.return_value = {
            "id": "fake_channel_id",
            "snippet": {
                "title": "updated channel title",
                "description": "channel description",
                "publishedAt": "2012-10-01T15:27:35.000Z",
            },
            "contentDetails": {
                "duration": "PT1H46M12S",
            },
        }

        out = StringIO()
        call_command('add_video', 'https://www.youtube.com/watch?v=video_code', stdout=out)
        output = out.getvalue()
        self.assertIn('Adding talk "fake_video_id"', output)
        self.assertIn('Adding channel "fake_channel_id"', output)
        self.assertIn('Updated channel "updated channel title"', output)
        self.assertIn('Updated talk "updated video title"', output)
