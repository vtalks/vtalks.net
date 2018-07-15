from django.core.management.base import BaseCommand

from talks.models import Talk


class Command(BaseCommand):
    help = 'Filger and update talks on the database.'

    def add_arguments(self, parser):
        parser.add_argument('query', type=str)
        parser.add_argument('--event-edition', type=str)


    def handle(self, *args, **options):
        query = options['query']
        self.stdout.write('Search talks for "%s"' % query)
        talks = Talk.objects.filter(title__contains=query).order_by('id')

        print("Found {} talks:".format(len(talks)))

        """
        for talk in talks:
            talk.event_edition_id = options['event_edition']
            talk.save()

            event_edition_title = talk.event_edition.title or ""
            out = "id: {:d} - code: {:s} - title: {:s} - edition: {:s}".format(talk.id, talk.code, talk.title, event_edition_title)
            print(out)
        """
