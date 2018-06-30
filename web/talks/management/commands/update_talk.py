from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from talks.management import talk
from talks.models import Talk

from youtube_data_api3.video import get_video_code
from youtube_data_api3.video import fetch_video_data


class Command(BaseCommand):
    help = 'Updates an existing Talk into the database, given its Youtube URL'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url_video', type=str)

    def handle(self, *args, **options):
        youtube_url_video = options['youtube_url_video']

        # Get code from youtube url
        video_code = ""
        try:
            video_code = get_video_code(youtube_url_video)
        except Exception:
            msg = "ERROR: Invalid URL video {:s}".format(youtube_url_video)
            self.stdout.write(self.style.ERROR(msg))
            return

        # Check if the talk is already on the database
        if not Talk.objects.filter(code=video_code).exists():
            msg = "ERROR: Talk {:s} is not present on the database".format(video_code)
            self.stdout.write(self.style.NOTICE(msg))

            # Call to create command instead
            management.call_command("create_video", youtube_url_video)
            return

        # Get the talk from the database
        talk_obj = Talk.objects.get(code=video_code)

        msg = "Updating talk code:{:s}".format(talk_obj.code)
        self.stdout.write(msg)

        # Fetch video data from Youtube API
        video_json_data = fetch_video_data(settings.YOUTUBE_API_KEY, talk_obj.code)

        # If no data is received un-publish the Talk
        if video_json_data is None:
            msg = "ERROR: Youtube Data API does not return anything for video {:s}".format(talk_obj.code)
            self.stdout.write(self.style.ERROR(msg))
            talk_obj.published = False
            talk.save()
            return

        # if uploadStatus on youtube is failed we un-publish the video
        if "status" in video_json_data:
            status = video_json_data['status']
            if "uploadStatus" in status:
                if status['uploadStatus'] == "failed":
                    msg = "ERROR: Youtube statusUpload is failed unpublish video {:s}".format(talk_obj.code)
                    self.stdout.write(self.style.ERROR(msg))
                    talk.published = False
                    talk.save()
                    return

        talk.update_talk(talk_obj, video_json_data)

        msg = "Talk id:{:d} - title:{:s} updated successfully".format(talk_obj.id, talk_obj.title)
        self.stdout.write(self.style.SUCCESS(msg))
