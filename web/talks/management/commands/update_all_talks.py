from datetime import date
from datetime import timedelta

from django.core import management
from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Update all talks on the database.'

    def handle(self, *args, **options):
        today = date.today()
        yesterday=today-timedelta(days=1)
        talks = Talk.published_objects.filter(updated__lte=yesterday).order_by('-updated')
        for talk in talks:
            management.call_command("update_talk", talk.youtube_url)
