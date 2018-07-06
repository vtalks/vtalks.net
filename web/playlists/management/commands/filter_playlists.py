from django.core.management.base import BaseCommand

from playlists.models import Playlist


class Command(BaseCommand):
    help = 'Filter Playlists from the database, given a query'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str)

    def handle(self, *args, **options):
        query = options['query']

        playlists = Playlist.objects.filter(title__contains=query)
        for playlist in playlists:
            out = "id:{:d} code:{:s} title:{:s}".format(playlist.id, playlist.code, playlist.title)
            print(out)
