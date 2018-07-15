from datetime import date
from datetime import timedelta

from django.core import management
from django.core.management.base import BaseCommand

from playlists.models import Playlist


class Command(BaseCommand):
    help = 'Update all playlists on the database.'

    def handle(self, *args, **options):
        today = date.today()
        yesterday = today - timedelta(days=1)
        playlists = Playlist.objects.filter(updated__lte=yesterday).order_by("-updated")
        for playlist in playlists:
            management.call_command("update_playlist", playlist.youtube_url)
