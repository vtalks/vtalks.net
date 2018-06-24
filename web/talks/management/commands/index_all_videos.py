import json
from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Index all videos on ElasticSearch.'

    def handle(self, *args, **options):
        talks = Talk.published_objects.all()[:1]
        for talk in talks:
            print(
                "Indexing video id:{:d} - code:{:s} - youtube_url:{:s}".format(
                    talk.id,
                    talk.code,
                    talk.youtube_url)
            )

            talk_json_data = json.dump(talk)
            print(talk_json_data)
