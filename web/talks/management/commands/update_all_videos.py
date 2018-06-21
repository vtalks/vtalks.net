from django.conf import settings
from django.core.management.base import BaseCommand

from talks.models import Talk
from youtube_data_api3.video import fetch_video_data


class Command(BaseCommand):
    help = 'Update all videos on the database.'

    def handle(self, *args, **options):
        talks = Talk.published_objects.all()
        for talk in talks:
            print(
                "Updating video id:{:d} - code:{:s} - youtube_url:{:s}".format(
                    talk.id,
                    talk.code,
                    talk.youtube_url)
            )

            # Fetch video data from Youtube API
            youtube_video_data = fetch_video_data(settings.YOUTUBE_API_KEY, talk.code)

            # if no data is received we un-publish the video
            if youtube_video_data is None:
                print("Un-publish video because youtube API does not return data")
                talk.published = False
                talk.save()
                exit(0)

            # if uploadStatus on youtube is failed we un-publish the video
            if "status" in youtube_video_data:
                status = youtube_video_data['status']
                if "uploadStatus" in status:
                    if status['uploadStatus'] == "failed":
                        print("Un-publish video because youtube statusUpload is failed")
                        talk.published = False
                        talk.save()
                        exit(0)

            talk.update_video_model(youtube_video_data)

            talk.update_video_tags(youtube_video_data)

            talk.update_video_statistics(youtube_video_data)

            talk.recalculate_video_sortrank()

            talk.save()

            print("Video updated successfully")
