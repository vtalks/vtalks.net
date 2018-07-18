import requests

from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Delete unpublished videos from ElasticSearch.'

    def handle(self, *args, **options):
        talks = Talk.objects.filter(published=False).order_by('-id')
        for talk in talks:
            elastic_search_index = "vtalks"
            elastic_search_type = "talk"
            url = "http://elasticsearch:9200/{:s}/{:s}/{:d}".format(elastic_search_index, elastic_search_type, talk.id)
            resp = requests.delete(url)
            if resp.status_code not in [200, 201]:
                print("ERROR: {:s}".format(url))
                print("ERROR: Status code {:d}".format(resp.status_code))
                print("ERROR: {:s}".format(resp.text))
                print("ERROR: {:s}".format(url))
                exit(1)

            print(
                "Video id:{:d} - code:{:s} - youtube_url:{:s} deleted successfully from the index".format(
                    talk.id,
                    talk.code,
                    talk.youtube_url)
            )
