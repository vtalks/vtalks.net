from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Filter Talks from the database, given a query'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str)

    def handle(self, *args, **options):
        query = options['query']

        talks = Talk.objects.filter(title__contains=query).order_by("id")

        print("Found {:d} talks:".format(len(talks)))

        for talk in talks:
            event_edition_title = talk.event_edition.title or ""
            out = "id: {:d} - code: {:s} - title: {:s} - edition: {:d}".format(talk.id, talk.code, talk.title, event_edition_title)
            print(out)
