import requests

from django.core.management.base import BaseCommand

from events.models import Event


class Command(BaseCommand):
    help = 'Import events from a confs.tech json file to the database.'

    def add_arguments(self, parser):
        parser.add_argument('input_url', type=str)

    def handle(self, *args, **options):
        input_url = options['input_url']
        input_json_data = requests.get(input_url).json()

        for event in input_json_data:
            print(event)
