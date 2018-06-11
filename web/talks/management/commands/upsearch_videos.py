from django.core.management.base import BaseCommand

from ...models import Talk


class Command(BaseCommand):
    help = 'Search and update videos on the database.'

    def add_arguments(self, parser):
        parser.add_argument('q', type=str)
        parser.add_argument('--event-edition', type=str)

    def handle(self, *args, **options):
        query = options['q']
        self.stdout.write('Search talks for "%s"' % query)
        talks = Talk.objects.filter(title__contains=query).order_by('updated')

        for talk in talks:
            self.stdout.write('Updating talk #{} "{}"'.format(talk.id,
                                                              talk.title))

            # Iterate over and update found talks
            talk.event_edition_id = options['event_edition']

            talk.save()
