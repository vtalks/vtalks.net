from datetime import date
from datetime import datetime
from datetime import timedelta

from django.utils import timezone
from django.core import management
from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Update all talks on the database.'

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today-timedelta(days=1)

        datetime_updated_at = datetime.strptime(str(yesterday), "%Y-%m-%d")
        datetime_updated_at = datetime_updated_at.replace(tzinfo=timezone.utc)

        talks = Talk.published_objects.filter(updated__lte=datetime_updated_at).order_by('-updated')
        for talk in talks:
            management.call_command("update_talk", talk.youtube_url)
