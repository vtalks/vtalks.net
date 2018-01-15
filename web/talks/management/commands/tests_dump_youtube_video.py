from unittest.mock import patch

from django.test import TestCase
from django.utils.six import StringIO
from django.core.management import call_command

# Create your tests here.


class DumpYoutubeVideoCommandTests(TestCase):

    @patch("talks.management.commands.dump_youtube_video.fetch_video_data")
    def test_command(self, fake_fetch_video_data):
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

        out = StringIO()
        call_command('dump_youtube_video', 'https://www.youtube.com/watch?v=video_code', stdout=out)
        output = out.getvalue()
        self.assertIn('Fetch talk "fake_video_id"', output)

