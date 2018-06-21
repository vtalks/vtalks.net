from django.conf import settings
from django.core.management.base import BaseCommand

from talks.models import Talk

from youtube_data_api3.video import get_video_code
from youtube_data_api3.video import fetch_video_data


class Command(BaseCommand):
    help = 'Update a video on the database.'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url_video', type=str)

    def handle(self, *args, **options):
        youtube_url_video = options['youtube_url_video']

        # Get code from youtube url
        video_code = ""
        try:
            video_code = get_video_code(youtube_url_video)
        except Exception:
            print("ERROR: Invalid youtube URL video {:s}".format(youtube_url_video))
            exit(1)

        # Get talk from the database
        talk = None
        try:
            talk = Talk.objects.get(code=video_code)
        except Talk.DoesNotExist:
            print("ERROR: Video does not exist on the database")
            exit(1)

        print("Updating video id:{:d} - code:{:s} - youtube_url:{:s}".format(
            talk.id,
            video_code,
            youtube_url_video)
        )

        # Fetch video data from Youtube API
        youtube_video_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        # if no data is received we unpublish the video
        if youtube_video_data is None:
            print("Mark video unpublished because youtube API does not return data")
            talk.published = False
            talk.save()
            exit(0)

        # if uploadStatus on youtube is failed we unpublish the video
        if youtube_video_data['status']['uploadStatus'] == "failed":
            print("Mark video unpublished because youtube statusUpload is failed")
            talk.published = False
            talk.save()
            exit(0)

        talk.update_video_model(youtube_video_data)

        # talk.update_video_tags()

        # talk.update_video_statistics()

        talk.recalculate_video_sortrank()

        # Save video to database
        talk.save()

        print("Video updated successfully")
