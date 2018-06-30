from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand

from talks.management import talk
from talks.models import Talk

from youtube_data_api3.video import get_video_code
from youtube_data_api3.video import fetch_video_data


class Command(BaseCommand):
    help = 'Create Talk into the database, given its Youtube URL'

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
        if Talk.objects.filter(code=video_code).exists():
            msg = "ERROR: Talk {:s} is already present on the database".format(talk_code)
            self.stdout.write(self.style.NOTICE(msg))

            # Call to update command instead
            management.call_command("update_talk", youtube_url_video)
            return

        msg = "Creating talk code:{:s}".format(video_code)
        self.stdout.write(msg)

        # Fetch channel data from Youtube API
        video_json_data = fetch_video_data(settings.YOUTUBE_API_KEY, video_code)

        # If no data is received do nothing
        if video_json_data is None:
            msg = "ERROR: Youtube Data API does not return anything for video {:s}".format(video_code)
            self.stdout.write(self.style.ERROR(msg))
            return

        talk_obj = talk.create_talk(video_json_data)

        msg = "Talk id:{:d} - title:{:s} created successfully".format(talk_obj.id, talk_obj.title)
        self.stdout.write(self.style.SUCCESS(msg))
