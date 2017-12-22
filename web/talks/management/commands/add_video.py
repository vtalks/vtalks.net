from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Adds a video to the system'

    def add_arguments(self, parser):
        parser.add_argument('youtube_url', nargs='+', type=str)

    def handle(self, *args, **options):
        print("add video!")
