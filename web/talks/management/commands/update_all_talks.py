from django.core import management
from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Update all videos on the database.'

    def handle(self, *args, **options):
        talks = Talk.published_objects.all().order_by('-updated')
        for talk in talks:
            management.call_command("update_talk", talk.youtube_url)
