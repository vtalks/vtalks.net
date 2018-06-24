import requests

from django.core.management.base import BaseCommand

from talks.models import Talk
from talks.api import TalkSerializer


class Command(BaseCommand):
    help = 'Index all videos on ElasticSearch.'

    def handle(self, *args, **options):
        talks = Talk.published_objects.all().order_by('id')
        for talk in talks:
            serializer = TalkSerializer(talk, many=False)
            talk_json_data = serializer.data

            url = "http://elasticsearch:9200/talk/_doc/{:d}".format(talk.id)
            resp = requests.put(url, json=talk_json_data)
            if resp.status_code not in [200, 201]:
                print("ERROR: {:s}".format(url))
                print("ERROR: Status code {:d}".format(resp.status_code))

            print(
                "Video id:{:d} - code:{:s} - youtube_url:{:s} indexed successfully".format(
                    talk.id,
                    talk.code,
                    talk.youtube_url)
            )
