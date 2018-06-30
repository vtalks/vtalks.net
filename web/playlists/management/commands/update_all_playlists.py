from django.core import management
from django.core.management.base import BaseCommand

from playlists.models import Playlist


class Command(BaseCommand):
    help = 'Update all playlists on the database.'

    def handle(self, *args, **options):
        playlists = Playlist.objects.all().order_by("updated")
        for playlist in playlists:
            management.call_command("update_playlist", playlist.youtube_url)
